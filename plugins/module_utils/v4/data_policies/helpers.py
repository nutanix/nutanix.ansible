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


def get_recovery_setting(module, api_instance, recovery_plan_ext_id, ext_id):
    """
    This method will return recovery setting info using external ID.
    Args:
        module: Ansible module
        api_instance: RecoveryPlansApi instance from ntnx_datapolicies_py_client sdk
        recovery_plan_ext_id (str): External identifier of the recovery plan
        ext_id (str): Recovery setting external ID
    Returns:
        recovery_setting_info (object): recovery setting info
    """
    try:
        return api_instance.get_recovery_setting_by_id(
            recoveryPlanExtId=recovery_plan_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery setting info using ext_id",
        )
