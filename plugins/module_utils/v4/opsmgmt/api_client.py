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
    import ntnx_opsmgmt_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    Return an authenticated ``ntnx_opsmgmt_py_client.ApiClient`` for the
    NCM Operation Base Platform (``opsmgmt``) namespace.

    Args:
        module (AnsibleModule): the calling Ansible module — the standard
            v2 connection parameters (``nutanix_host``, ``nutanix_port``,
            ``nutanix_username``/``nutanix_password`` or
            ``nutanix_api_key``, ``validate_certs``, ``read_timeout``,
            proxy fields) are read from ``module.params``.

    Returns:
        ntnx_opsmgmt_py_client.ApiClient: a configured client with
        Basic-Auth (or API-key) headers, proxy settings, and version
        negotiation applied.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_opsmgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    config = ntnx_opsmgmt_py_client.Configuration()
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
    try:
        client = ntnx_opsmgmt_py_client.ApiClient(
            configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
        )
    except TypeError:
        client = ntnx_opsmgmt_py_client.ApiClient(configuration=config)
    config.read_timeout = module.params.get("read_timeout")
    _apply_proxy_from_env(config, module)
    client = ntnx_opsmgmt_py_client.ApiClient(
        configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
    )
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
    Extract the HTTP ETag from an opsmgmt v4 API response envelope.

    Args:
        data: opsmgmt v4 API response body (typically the top-level
            ``*ApiResponse`` object returned by an SDK call).

    Returns:
        str | None: the ETag value if the response carries one, otherwise
        ``None`` (which callers should treat as "no optimistic locking
        header available").
    """
    return ntnx_opsmgmt_py_client.ApiClient.get_etag(data)


def get_report_artifacts_api_instance(module):
    """
    Return a ``ReportArtifactsApi`` instance bound to a fresh opsmgmt
    ApiClient built from ``module``.

    This is the only entry point modules should use to talk to the
    ReportArtifacts endpoints (``/api/opsmgmt/v4.1.b1/content/report-artifacts``)
    so credentials, proxy configuration, and logging stay consistent
    across modules.

    Args:
        module (AnsibleModule): the calling Ansible module.

    Returns:
        ntnx_opsmgmt_py_client.ReportArtifactsApi: SDK API instance ready
        for create / list / upload / download calls.
    """
    api_client = get_api_client(module)
    return ntnx_opsmgmt_py_client.ReportArtifactsApi(api_client=api_client)
