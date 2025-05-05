# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_routing_policy(module, api_instance, ext_id):
    """
    This method will return routing policy info using its ext_id
    Args:
        module: Ansible module
        api_instance: RoutingPoliciesApi instance from ntnx_networking_py_client sdk
        ext_id (str): routing policy info external ID
    return:
        info (object): routing policy info
    """
    try:
        return api_instance.get_routing_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching routing policy info using ext_id",
        )


def get_floating_ip(module, api_instance, ext_id):
    """
    Get Floating ip by ext_id
    Args:
        module: Ansible module
        api_instance: FloatingIpsApi instance from ntnx_networking_py_client sdk
        ext_id: ext_id of Floating ip
    Returns:
        floating_ip (obj): Floating ip info object
    """
    try:
        return api_instance.get_floating_ip_by_id(extId=ext_id).data

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching floating_ip info using ext_id",
        )


def get_vpc(module, api_instance, ext_id):
    """
    Get vpc by ext_id
    Args:
        module: Ansible module
        api_instance: VpcsApi instance from ntnx_networking_py_client sdk
        ext_id: ext_id of vpc
    Returns:
        vpc (obj): Vpc info object
    """
    try:
        return api_instance.get_vpc_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vpc info using ext_id",
        )


def get_subnet(module, api_instance, ext_id):
    """
    This method will return subnet info using subnet external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Api client instance
        ext_id (str): subnet external ID
    return:
        subnet_info (object): subnet info
    """
    try:
        return api_instance.get_subnet_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching subnet info using ext_id",
        )


def get_route_table(module, api_instance, ext_id):
    """
    This method will return route table info using route table external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Route table API instance from SDK
        ext_id (str): route table external ID
    return:
        subnet_info (object): route table info
    """
    try:
        return api_instance.get_route_table_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route table info using ext_id",
        )


def get_route(module, api_instance, ext_id, route_table_ext_id):
    """
    This method will return route info using route external ID and table external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Route API instance from SDK
        ext_id (str): route external ID
        route_table_ext_id (str): route table external ID
    return:
        route_info (object): route info
    """
    try:
        return api_instance.get_route_for_route_table_by_id(
            extId=ext_id, routeTableExtId=route_table_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route info using ext_id and table ext_id",
        )
