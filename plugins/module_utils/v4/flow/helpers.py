# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_network_security_policy(module, api_instance, ext_id):
    """
    This method will return network security rule info using external ID.
    Args:
        module: Ansible module
        api_instance: NetworkSecurityPoliciesApi instance from ntnx_microseg_py_client sdk
        ext_id (str): network security rule info external ID
    return:
        security_policy_info (object): network security rule info
    """
    try:
        return api_instance.get_network_security_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network security rule info using ext_id",
        )


def get_service_group(module, api_instance, ext_id):
    """
    This method will return service group info using external ID.
    Args:
        module: Ansible module
        api_instance: ServiceGroupsApi instance from ntnx_microseg_py_client sdk
        ext_id (str): service group info external ID
    return:
        service_group_info (object): service group info
    """
    try:
        return api_instance.get_service_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching service group info using ext_id",
        )


def get_address_group(module, api_instance, ext_id):
    """
    This method will return address group info using external ID.
    Args:
        module: Ansible module
        api_instance: AddressGroupsApi instance from ntnx_microseg_py_client sdk
        ext_id (str): address group info external ID
    return:
        address_group_info (object): address group info
    """
    try:
        return api_instance.get_address_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching address group info using ext_id",
        )


def strip_service_group_extra_attributes(obj):
    """
    This method will remove antivirus object's extra fields from given object.
    Args:
        obj (object): antivirus object
    """

    extra_fields = ["is_system_defined"]

    for field in extra_fields:
        setattr(obj, field, None)

    return obj
