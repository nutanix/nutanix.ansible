from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_authorization_policy(module, api_instance, ext_id):
    """
    This method will return authorization policy info using ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): Authorization policy api instance
        ext_id (str): External id of authorization policy
    Returns:
        authorization_policy_info (dict): Authorization policy info
    """
    try:
        return api_instance.get_authorization_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching authorization policy using ext_id",
        )


def get_role(module, api_instance, ext_id):
    """
    This method will return role info using ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): Role api instance
        ext_id (str): External id of role
    Returns:
        role_info (dict): Role info
    """
    try:
        return api_instance.get_role_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching role info using ext_id",
        )


def get_permission(module, api_instance, ext_id):
    """
    This method will return permission info using ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): Permission api instance
        ext_id (str): External id of permission
    Returns:
        permission_info (dict): Permission info
    """
    try:
        return api_instance.get_operation_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching permission info",
        )


def get_user_group(module, api_instance, ext_id):
    """
    This method will return user group info using ext_id.
    Args:
        module (AnsibleModule): Ansible module object
        api_instance (ApiClient): ApiClient object
        ext_id (str): External ID of the user group
    Returns:
        user_group_info (dict): User group info
    """
    try:
        return api_instance.get_user_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user group info",
        )


def get_user(module, api_instance, ext_id):
    """
    This method will return user info using ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): User api instance
        ext_id (str): External id of user
    Returns:
        user_info (dict): User info
    """
    try:
        return api_instance.get_user_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user info",
        )


def get_identity_provider(module, api_instance, ext_id):
    """
    Get identity provider by ext_id
    Args:
        module: Ansible module
        api_instance: SAMLIdentityProvidersApi instance from ntnx_iam_py_client sdk
        ext_id: External id of identity provider
    Returns:
        identity provider (obj): identity provider info object
    """
    try:
        return api_instance.get_saml_identity_provider_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching directory service info",
        )


def get_directory_service(module, api_instance, ext_id):
    """
    This method will return directory service info using ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): Directory service api instance
        ext_id (str): External id of directory service
    Returns:
        directory_service_info (dict): Directory service info
    """
    try:
        return api_instance.get_directory_service_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching directory service info",
        )
