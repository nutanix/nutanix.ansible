from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_vm_recovery_point(
    module, api_instance, recovery_point_ext_id, vm_recovery_point_ext_id
):
    """
    This method will return vm recovery point info which is part of given top level recovery_point_ext_id
    Args:
        module: Ansible module
        api_instance: VmRecoveryPointsApi instance from ntnx_dataprotection_py_client sdk
        recovery_point_ext_id (str): top level recovery point external ID
        vm_recovery_point_ext_id (str): vm recovery point external ID
    Returns:
        vm_recovery_point_info (object): vm recovery point info
    """
    try:
        return api_instance.get_vm_recovery_point_by_id(
            recoveryPointExtId=recovery_point_ext_id, extId=vm_recovery_point_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm recovery point info using ext_id",
        )


def get_recovery_point(module, api_instance, ext_id):
    """
    This method will return recovery point info using external ID.
    Args:
        module: Ansible module
        api_instance: AddressGroupsApi instance from ntnx_dataprotection_py_client sdk
        ext_id (str): top level recovery point external ID
    Returns:
        recovery_point_info (object): recovery point info
    """
    try:
        return api_instance.get_recovery_point_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery point info using ext_id",
        )
