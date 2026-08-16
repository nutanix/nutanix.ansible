# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

from ...constants import ALLOW_VERSION_NEGOTIATION
from ..api_logger import setup_api_logging
from ..utils import _apply_proxy_from_env

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    Return an authenticated ntnx_storage_py_client.ApiClient using the module's
    connection parameters.

    Args:
        module: The Ansible module instance whose ``params`` supply the Prism
            Central host, credentials, TLS validation, and read-timeout values.

    Returns:
        ntnx_storage_py_client.ApiClient: An API client wired up with basic
        auth (or API key), proxy support from the environment, and API request
        logging when debug is enabled.
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
            configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
        )
    except TypeError:
        # Older versions of ntnx_storage_py_client do not accept
        # allow_version_negotiation; fall back to the plain constructor.
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

    return client


def get_etag(data):
    """
    Return the ETag value from a v4 storage API response object.

    Args:
        data: A v4 API response object returned by ntnx_storage_py_client.

    Returns:
        str: The ETag string, suitable for passing back as ``If-Match`` on the
        next update.
    """
    return ntnx_storage_py_client.ApiClient.get_etag(data)


def get_vg_api_instance(module):
    """
    Return a ``VolumeGroupApi`` instance from the storage SDK.

    Args:
        module: The Ansible module instance used to build the API client.

    Returns:
        ntnx_storage_py_client.VolumeGroupApi: An API stub for the storage
        namespace's Volume Group endpoints (including the metadata-info sub
        resource).
    """
    client = get_api_client(module)
    return ntnx_storage_py_client.VolumeGroupApi(api_client=client)
