# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"), exception=SDK_IMP_ERROR
        )

    config = ntnx_microseg_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    config.proxy_scheme = module.params.get("proxy_scheme")
    config.proxy_host = module.params.get("proxy_host")
    config.proxy_port = module.params.get("proxy_port")
    client = ntnx_microseg_py_client.ApiClient(configuration=config)

    cred = "{0}:{1}".format(config.username, config.password)
    try:
        encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
    except BaseException:
        encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
    auth_header = "Basic " + encoded_cred
    client.add_default_header(header_name="Authorization", header_value=auth_header)
    return client


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    Returns:
        str: etag value
    """
    return ntnx_microseg_py_client.ApiClient.get_etag(data)


def get_service_groups_api_instance(module):
    """
    This method will return service groups api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): service group api instance
    """
    client = get_api_client(module)
    return ntnx_microseg_py_client.ServiceGroupsApi(client)


def get_address_groups_api_instance(module):
    """
    This method will return address groups api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): address group api instance
    """
    client = get_api_client(module)
    return ntnx_microseg_py_client.AddressGroupsApi(client)


def get_network_security_policy_api_instance(module):
    """
    This method will return NetworkSecurityPoliciesApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): network security rule api instance
    """
    client = get_api_client(module)
    return ntnx_microseg_py_client.NetworkSecurityPoliciesApi(client)
