# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_protection_policy(module, api_instance, ext_id):
    """
    This method will return protection policy info using external ID.
    Args:
        module: Ansible module
        api_instance: ProtectionPoliciesApi instance from ntnx_datapolicies_py_client sdk
        ext_id (str): Protection policy external ID
    Returns:
        protection_policy_info (object): protection policy info
    """
    try:
        return api_instance.get_protection_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching protection policy info using ext_id",
        )


def get_storage_policy(module, api_instance, ext_id):
    """
    This method will return storage policy info using external ID.
    Args:
        module: Ansible module
        api_instance: StoragePoliciesApi instance from ntnx_datapolicies_py_client sdk
        ext_id (str): Storage policy external ID
    Returns:
        storage_policy_info (object): storage policy info
    """
    try:
        return api_instance.get_storage_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage policy info using ext_id",
        )


def get_consistency_rule(module, api_instance, protection_policy_ext_id, ext_id):
    """
    This method will return a consistency rule using its external ID.
    Args:
        module: Ansible module
        api_instance: ProtectionPoliciesApi instance from ntnx_datapolicies_py_client
        protection_policy_ext_id (str): External ID of the parent protection policy
        ext_id (str): External ID of the consistency rule
    Returns:
        consistency_rule_info (object): consistency rule info
    """
    try:
        return api_instance.get_consistency_rule_by_id(
            protectionPolicyExtId=protection_policy_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching consistency rule info using ext_id",
        )


def get_consistency_rule_by_name(module, api_instance, protection_policy_ext_id, name):
    """
    Find a consistency rule under a protection policy by its name.
    Args:
        module: Ansible module
        api_instance: ProtectionPoliciesApi instance
        protection_policy_ext_id (str): External ID of the parent protection policy
        name (str): Name of the consistency rule
    Returns:
        object or None: The matching consistency rule or None if not found.
    """
    try:
        resp = api_instance.list_consistency_rules_by_protection_policy_id(
            protectionPolicyExtId=protection_policy_ext_id,
            _filter="name eq '{0}'".format(name),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing consistency rules by name",
        )
    data = getattr(resp, "data", None) or []
    for item in data:
        if getattr(item, "name", None) == name:
            return item
    return None
