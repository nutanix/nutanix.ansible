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
    Build an :class:`ntnx_opsmgmt_py_client.ApiClient` from the module's
    connection parameters. Follows the same pattern used by the networking /
    vmm helpers in this collection.

    Args:
        module (AnsibleModule): The module instance whose params contain the
            connection details (host, port, credentials, proxy, TLS options).

    Returns:
        ntnx_opsmgmt_py_client.ApiClient: A ready-to-use API client with
        authentication, TLS verification, proxy handling, and request logging
        wired up.
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
    Extract the ETag value from a v4 API response object.

    The v4 SDK stores the ETag in the response's ``_reserved`` metadata; this
    helper delegates to :meth:`ApiClient.get_etag` which already knows how to
    read it. Consumers pass the resulting string to update / delete calls via
    the ``if_match`` keyword argument.

    Args:
        data: A v4 response object (typically the ``.data`` attribute of an
            API response).

    Returns:
        str | None: The ETag string, or ``None`` if the response does not
        carry one.
    """
    return ntnx_opsmgmt_py_client.ApiClient.get_etag(data)


def get_global_report_setting_api_instance(module):
    """
    Build and return a :class:`GlobalReportSettingApi` client.

    Args:
        module (AnsibleModule): The module whose connection parameters are
            used to construct the underlying API client.

    Returns:
        ntnx_opsmgmt_py_client.GlobalReportSettingApi: An API instance ready
        to invoke Get / Update on the per-user global report setting.
    """
    api_client = get_api_client(module)
    return ntnx_opsmgmt_py_client.GlobalReportSettingApi(api_client=api_client)
