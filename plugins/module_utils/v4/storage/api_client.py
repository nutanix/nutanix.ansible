# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import ssl
import traceback
import uuid
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six.moves.urllib.request import (
    HTTPSHandler,
    Request,
    build_opener,
)

from ...constants import ALLOW_VERSION_NEGOTIATION
from ..api_logger import setup_api_logging
from ..utils import _apply_proxy_from_env

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


_SDK_STORAGE_VERSION = "v4.0.a4"
_CANDIDATE_VERSIONS = ["v4.0.a4", "v4.0.a3", "v4.0.a2", "v4.0.a1"]


def _probe_supported_storage_version(module):
    """Probe the Prism Central endpoint to find the supported storage v4 version.

    We POST an empty body to ``storage-containers`` for each candidate version.
    A ``404`` means the endpoint does not exist for that version, whereas any
    other status (e.g. ``400`` for missing fields) indicates the endpoint
    exists. The first version yielding a non-404 status wins.
    """
    host = module.params.get("nutanix_host")
    port = module.params.get("nutanix_port") or 9440
    username = module.params.get("nutanix_username")
    password = module.params.get("nutanix_password")
    verify = module.params.get("validate_certs", True)

    ssl_ctx = ssl.create_default_context()
    if not verify:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    base_url = "https://{0}:{1}".format(host, port)
    if not (username and password):
        return None
    try:
        token = b64encode("{0}:{1}".format(username, password).encode("ascii")).decode(
            "ascii"
        )
    except Exception:
        return None
    auth_header = "Basic " + token
    opener = build_opener(HTTPSHandler(context=ssl_ctx))

    for version in _CANDIDATE_VERSIONS:
        url = "{0}/api/storage/{1}/config/storage-containers".format(base_url, version)
        try:
            req = Request(
                url,
                method="POST",
                data=b"{}",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": auth_header,
                },
            )
            resp = opener.open(req, timeout=15)
            if resp.status != 404:
                return version
        except HTTPError as exc:
            if exc.code != 404:
                return version
        except Exception:
            continue
    return None


_STORAGE_LIST_PATH_RE = re.compile(
    r"^/api/storage/{0}/config/storage-containers/?$".format(
        re.escape(_SDK_STORAGE_VERSION)
    )
)
_STORAGE_STATS_PATH_RE = re.compile(
    r"^/api/storage/{0}/stats/storage-containers/".format(
        re.escape(_SDK_STORAGE_VERSION)
    )
)


def _install_version_shim(client, target_version):
    """Rewrite outgoing URLs from the SDK-hardcoded ``v4.0.a4`` to the
    version supported by the PC. When the storage namespace does not expose
    per-container endpoints, fall back transparently to the ``clustermgmt``
    namespace which has an identical schema, injecting the
    ``NTNX-Request-Id`` idempotency header required by that endpoint.

    ``target_version`` is used for list / POST endpoints; the
    ``clustermgmt/v4.3`` namespace is used for per-container operations.
    """
    private_name = "_ApiClient__call_api"
    original = getattr(client, private_name, None)
    if original is None:
        return

    list_replacement = "/api/storage/{0}/".format(
        target_version or _SDK_STORAGE_VERSION
    )
    item_replacement = "/api/clustermgmt/v4.3/"
    sdk_prefix = "/api/storage/{0}/".format(_SDK_STORAGE_VERSION)

    def wrapped(resource_path, method, *args, **kwargs):
        rewritten = resource_path
        if resource_path.startswith(sdk_prefix):
            if _STORAGE_LIST_PATH_RE.match(
                resource_path
            ) or _STORAGE_STATS_PATH_RE.match(resource_path):
                rewritten = resource_path.replace(sdk_prefix, list_replacement)
            else:
                rewritten = resource_path.replace(sdk_prefix, item_replacement)
                header_params = None
                if len(args) >= 3:
                    header_params = args[2]
                else:
                    header_params = kwargs.get("header_params")
                if header_params is None:
                    header_params = {}
                    if len(args) >= 3:
                        args = list(args)
                        args[2] = header_params
                        args = tuple(args)
                    else:
                        kwargs["header_params"] = header_params
                if "NTNX-Request-Id" not in header_params:
                    header_params["NTNX-Request-Id"] = str(uuid.uuid4())
        return original(rewritten, method, *args, **kwargs)

    setattr(client, private_name, wrapped)


def get_api_client(module):
    """Return an authenticated ntnx_storage_py_client.ApiClient built from
    module connection parameters.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    config = ntnx_storage_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    api_key = module.params.get("nutanix_api_key")
    nutanix_username = module.params.get("nutanix_username")
    nutanix_password = module.params.get("nutanix_password")
    if (not nutanix_username or not nutanix_password) and not api_key:
        module.fail_json(
            msg="Either nutanix_username and nutanix_password or nutanix_api_key is required"
        )
    if api_key:
        config.set_api_key(api_key)
    else:
        config.username = nutanix_username
        config.password = nutanix_password
    config.verify_ssl = module.params.get("validate_certs")
    config.read_timeout = module.params.get("read_timeout")
    _apply_proxy_from_env(config, module)

    try:
        client = ntnx_storage_py_client.ApiClient(
            configuration=config,
            allow_version_negotiation=ALLOW_VERSION_NEGOTIATION,
        )
    except TypeError:
        client = ntnx_storage_py_client.ApiClient(configuration=config)

    if not api_key:
        cred = "{0}:{1}".format(config.username, config.password)
        try:
            encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
        except BaseException:
            encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
        auth_header = "Basic " + encoded_cred
        client.add_default_header(header_name="Authorization", header_value=auth_header)

    setup_api_logging(module, client)

    negotiated = _probe_supported_storage_version(module) or _SDK_STORAGE_VERSION
    _install_version_shim(client, negotiated)

    return client


def get_etag(data):
    """Return the etag from a storage v4 API response payload."""
    return ntnx_storage_py_client.ApiClient.get_etag(data)


def get_storage_container_api_instance(module):
    """Return the StorageContainerApi instance from ntnx_storage_py_client."""
    client = get_api_client(module)
    return ntnx_storage_py_client.StorageContainerApi(api_client=client)
