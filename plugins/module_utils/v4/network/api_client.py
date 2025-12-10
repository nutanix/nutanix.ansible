# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

from ..api_logger import setup_api_logging

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    Args:
        module (object): Ansible module object
    return:
        client (object): api client object
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    config = ntnx_networking_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    client = ntnx_networking_py_client.ApiClient(configuration=config)

    cred = "{0}:{1}".format(config.username, config.password)
    try:
        encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
    except BaseException:
        encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
    auth_header = "Basic " + encoded_cred
    client.add_default_header(header_name="Authorization", header_value=auth_header)

    # Setup API logging if debug is enabled
    setup_api_logging(module, client)

    return client


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    return:
        etag (str): etag value
    """
    return ntnx_networking_py_client.ApiClient.get_etag(data)


def get_routing_policies_api_instance(module):
    """
    This method will return RoutingPoliciesApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): routing policies api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.RoutingPoliciesApi(api_client=api_client)


def get_floating_ip_api_instance(module):
    """
    This method will return FloatingIpsApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): floating ip api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.FloatingIpsApi(api_client=api_client)


def get_vpc_api_instance(module):
    """
    This method will return VpcsApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): vpc api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.VpcsApi(api_client=api_client)


def get_subnet_api_instance(module):
    """
    This method will return subnet api instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): subnet api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.SubnetsApi(api_client=api_client)


def get_route_tables_api_instance(module):
    """
    This method will return RouteTablesApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): route tables api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.RouteTablesApi(api_client=api_client)


def get_routes_api_instance(module):
    """
    This method will return RoutesApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): routes api instance
    """
    api_client = get_api_client(module)
    return ntnx_networking_py_client.RoutesApi(api_client=api_client)
