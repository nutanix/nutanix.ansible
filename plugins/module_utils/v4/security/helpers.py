# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_kms_by_ext_id(module, api_instance, ext_id):
    """
    This method will return Key Management Server info using external ID.
    Args:
        module: Ansible module
        api_instance: Key Management Server Api instance from ntnx_security_py_client sdk
        ext_id: External ID of the Key Management Server
    """
    try:
        return api_instance.get_key_management_server_by_id(ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Key Management Server info using external ID",
        )


def get_credential_by_ext_id(module, api_instance, ext_id):
    """
    This method will return Credential info using external ID.
    Args:
        module: Ansible module
        api_instance: Credentials Api instance from ntnx_security_py_client sdk
        ext_id: External ID of the Credential
    """
    try:
        return api_instance.get_credential_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Credential info using external ID",
        )


def get_security_configs_visibility_setting(module, api_instance, select=None):
    """
    This method will return the security configurations visibility setting.
    Args:
        module: Ansible module
        api_instance: SecurityConfigsVisibilityApi instance
        select: Optional OData $select expression
    """
    try:
        kwargs = {}
        if select is not None:
            kwargs["_select"] = select
        return api_instance.get_security_configs_visibility_setting(**kwargs).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching security configs visibility setting",
        )


def get_approval_policy_by_ext_id(module, api_instance, ext_id, select=None):
    """
    This method will return Approval Policy info using external ID.
    Args:
        module: Ansible module
        api_instance: ApprovalPoliciesApi instance
        ext_id: External ID of the Approval Policy
        select: Optional OData $select expression
    """
    try:
        kwargs = {}
        if select is not None:
            kwargs["_select"] = select
        return api_instance.get_approval_policy_by_ext_id(extId=ext_id, **kwargs).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Approval Policy info using external ID",
        )


def get_security_profile_by_ext_id(module, api_instance, ext_id):
    """
    This method will return Security Profile info using external ID.
    Args:
        module: Ansible module
        api_instance: SecurityProfilesApi instance
        ext_id: External ID of the Security Profile
    """
    try:
        return api_instance.get_security_profile_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Security Profile info using external ID",
        )


def get_advanced_config_by_security_profile_ext_id(
    module, api_instance, security_profile_ext_id
):
    """
    This method will return advanced config for a security profile.
    Args:
        module: Ansible module
        api_instance: SecurityProfilesApi instance
        security_profile_ext_id: External ID of the Security Profile
    """
    try:
        return api_instance.get_advanced_config(
            securityProfileExtId=security_profile_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching advanced config using security profile external ID",
        )
