# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_lcm_status(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM status info.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM status api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_status_info (dict): LCM status info
    """
    try:
        return api_instance.get_status(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM status info",
        )


def get_lcm_config(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM config info.
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
            msg="Api Exception raised while fetching LCM config info",
        )


def get_lcm_entity(module, api_instance, ext_id):
    """
    This method will return entity info using external identifier of the entity.
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
            msg="Api Exception raised while fetching entity info using external identifier of the entity",
        )


def get_claim_token(module, api_instance, ext_id):
    """
    This method will return a Foundation Central claim token using its ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): ClaimTokensApi instance
        ext_id (str): External id of the claim token
    Returns:
        claim_token (object): Claim token info object
    """
    try:
        return api_instance.get_claim_token_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching claim token info using ext_id",
        )
