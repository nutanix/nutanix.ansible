from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_restore_source(module, api_instance, ext_id):
    """
    This method will return restore source info using external ID.
    Args:
        module: Ansible module
        api_instance: DomainManagerBackupApi instance from ntnx_prism_py_client sdk
        ext_id (str): restore source info external ID
    return:
        restore_source_info (object): restore source info
    """
    try:
        return api_instance.get_restore_source_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restore source info using ext_id",
        )


def get_backup_target(module, api_instance, ext_id):
    """
    This method will return backup target info using external ID.
    Args:
        module: Ansible module
        api_instance: DomainManagerBackupApi instance from ntnx_prism_py_client sdk
        ext_id (str): backup target info external ID
    return:
        backup_target_info (object): backup target info
    """
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    try:
        return api_instance.get_backup_target_by_id(
            extId=ext_id, domainManagerExtId=domain_manager_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching backup target info using ext_id and domain_manager_ext_id",
        )


def get_pc_config(module, api_instance, ext_id):
    """
    This method will return pc config info using external ID.
    Args:
        module: Ansible module
        api_instance: DomainManagerBackupApi instance from ntnx_prism_py_client sdk
        ext_id (str): pc external ID
    return:
        pc_config_info (object): pc config info
    """
    try:
        return api_instance.get_domain_manager_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching pc config info using ext_id",
        )


def get_restore_point(
    module,
    api_instance,
    ext_id,
    restore_source_ext_id,
    restorable_domain_manager_ext_id,
):
    """
    This method will return restore point info using external ID.
    Args:
        module: Ansible module
        api_instance: DomainManagerBackupApi instance from ntnx_prism_py_client sdk
        ext_id (str): restore point info external ID
    return:
        restore_point_info (object): restore point info
    """
    try:
        return api_instance.get_restore_point_by_id(
            restoreSourceExtId=restore_source_ext_id,
            restorableDomainManagerExtId=restorable_domain_manager_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restore point info using ext_id",
        )
