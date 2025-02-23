from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_lcm_status(module, api_instance, ext_id):
    """
    This method will return LCM status info using cluster external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM status api instance
        ext_id (str): External id of cluster
    Returns:
        lcm_status_info (dict): LCM status info
    """
    try:
        return api_instance.get_status(X_Cluster_Id=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM status info using cluster external ID",
        )


def get_lcm_config(module, api_instance, cluster_ext_id):
    """
    This method will return LCM config info using cluster external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM config api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_config_info (dict): LCM config info
    """
    try:
        return api_instance.get_config(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM config info using cluster external ID",
        )


def get_lcm_entity(module, api_instance, ext_id):
    """
    This method will return entity info using external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Entity api instance
        ext_id (str): External id of entity
    Returns:
        entity_info (dict): Entity info
    """
    try:
        return api_instance.get_entity_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entity info using external identifier",
        )
