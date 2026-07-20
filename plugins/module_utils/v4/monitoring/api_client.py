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
    import ntnx_monitoring_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    Return a Nutanix monitoring v4 SDK ``ApiClient`` initialised from the
    Ansible module connection parameters (``nutanix_host``,
    ``nutanix_username``/``nutanix_password`` or ``nutanix_api_key``,
    ``nutanix_port``, ``validate_certs``, ``read_timeout``) plus any HTTP
    proxy settings.
    Args:
        module (AnsibleModule): running Ansible module instance.
    Returns:
        ntnx_monitoring_py_client.ApiClient: configured client for the
        monitoring v4 SDK.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_monitoring_py_client"),
            exception=SDK_IMP_ERROR,
        )

    config = ntnx_monitoring_py_client.Configuration()
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
        client = ntnx_monitoring_py_client.ApiClient(
            configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
        )
    except TypeError:
        client = ntnx_monitoring_py_client.ApiClient(configuration=config)
    config.read_timeout = module.params.get("read_timeout")
    _apply_proxy_from_env(config, module)
    client = ntnx_monitoring_py_client.ApiClient(
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
    Return the ETag header value for a v4 monitoring SDK response.
    Args:
        data (object): v4 monitoring SDK response object.
    Returns:
        str | None: ETag value if present, otherwise ``None``.
    """
    return ntnx_monitoring_py_client.ApiClient.get_etag(data)


def get_system_defined_checks_api_instance(module):
    """
    Return a ``SystemDefinedChecksApi`` instance bound to the shared
    monitoring ``ApiClient``. Use for the ``run-system-defined-checks``
    action endpoint.
    Args:
        module (AnsibleModule): running Ansible module instance.
    Returns:
        ntnx_monitoring_py_client.SystemDefinedChecksApi: SDK API handle.
    """
    api_client = get_api_client(module)
    return ntnx_monitoring_py_client.SystemDefinedChecksApi(api_client=api_client)


def get_system_defined_policies_api_instance(module):
    """
    Return a ``SystemDefinedPoliciesApi`` instance bound to the shared
    monitoring ``ApiClient``. Use for SDA (system-defined alert policy)
    read / list / update-cluster-config endpoints, and to resolve the
    ``sda_ext_ids`` accepted by the ``run-system-defined-checks`` action.
    Args:
        module (AnsibleModule): running Ansible module instance.
    Returns:
        ntnx_monitoring_py_client.SystemDefinedPoliciesApi: SDK API handle.
    """
    api_client = get_api_client(module)
    return ntnx_monitoring_py_client.SystemDefinedPoliciesApi(api_client=api_client)
