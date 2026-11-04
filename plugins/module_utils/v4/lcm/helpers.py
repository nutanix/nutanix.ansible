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


def get_node(module, api_instance, ext_id):
    """
    This method will return node info using external identifier of the node.

    The Nodes APIs are served by Foundation Central (FCVM/Foundation).
    Args:
        module (object): Ansible module object
        api_instance (object): Nodes api instance
        ext_id (str): External id of the node
    Returns:
        node_info (object): Node info (raw v4 api response with etag headers)
    """
    try:
        return api_instance.get_node_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching node info using external ID: {0}".format(
                ext_id
            ),
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


def get_lcm_bundle(module, api_instance, ext_id):
    """
    This method will return LCM bundle info using external identifier of the bundle.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM Bundles api instance
        ext_id (str): External id of the LCM bundle
    Returns:
        bundle_info (object): LCM bundle info
    """
    try:
        return api_instance.get_bundle_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM bundle info using ext_id {0}".format(
                ext_id
            ),
        )


def get_foundation_central_config(module, api_instance):
    """
    This method will return the Foundation Central configuration.
    Args:
        module (object): Ansible module object
        api_instance (object): Foundation Central config api instance
    Returns:
        foundation_central_config (object): Foundation Central config data
    """
    try:
        return api_instance.get_foundation_central_config().data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Foundation Central config info",
        )


def get_upgrade_selection(module, api_instance, ext_id):
    """
    This method fetches details of a single LCM Upgrade Selection using its external id.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM UpgradeSelections api instance
        ext_id (str): External id of the LCM Upgrade Selection
    Returns:
        upgrade_selection (object): LCM Upgrade Selection SDK object
    """
    try:
        return api_instance.get_upgrade_selection_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM upgrade selection with ext_id: {0}".format(
                ext_id
            ),
        )


def get_lcm_summary(module, api_instance, ext_id):
    """
    This method will return the LCM summary for a specific cluster using its
    external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): LcmSummaries api instance
        ext_id (str): External id of the LCM summary (cluster UUID)
    Returns:
        lcm_summary_info (object): LCM summary info
    """
    try:
        return api_instance.get_lcm_summary_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM summary with ext_id: {0}".format(
                ext_id
            ),
        )


def get_lcm_history(module, api_instance, ext_id):
    """
    This method will return an LCM history entry using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM histories api instance
        ext_id (str): External id of the LCM history entry
    Returns:
        lcm_history_info (dict): LCM history info
    """
    try:
        return api_instance.get_lcm_history_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM history with ext_id: {0}".format(
                ext_id
            ),
        )


def get_lcm_recommendation(module, api_instance, ext_id):
    """
    This method will return LCM update recommendation info using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM Recommendations api instance
        ext_id (str): External id of the recommendation resource
    Returns:
        recommendation_info (object): LCM recommendation info
    """
    try:
        return api_instance.get_recommendation_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM recommendation using external identifier",
        )


def get_lcm_notification(module, api_instance, ext_id):
    """
    This method will fetch an LCM upgrade notification using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM notifications api instance
        ext_id (str): External id of the LCM upgrade notification resource
    Returns:
        notification (object): LCM notification info
    """
    try:
        return api_instance.get_notification_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM notification with ext_id: {0}".format(
                ext_id
            ),
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


def get_claim_token_secret(module, api_instance, ext_id):
    """
    This method will return the secret for a Foundation Central claim token.
    Args:
        module (object): Ansible module object
        api_instance (object): ClaimTokensApi instance
        ext_id (str): External id of the claim token
    Returns:
        claim_token_secret (object): Claim token secret info object
    """
    try:
        return api_instance.get_secret_by_claim_token_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching claim token secret",
        )


def get_node_by_claim_token(module, api_instance, claim_token_ext_id, node_ext_id):
    """
    This method will return a node registered with a Foundation Central claim token.
    Args:
        module (object): Ansible module object
        api_instance (object): ClaimTokensApi instance
        claim_token_ext_id (str): External id of the claim token
        node_ext_id (str): External id of the node
    Returns:
        node (object): Node registered with the claim token
    """
    try:
        return api_instance.get_node_by_claim_token_id(
            claimTokenExtId=claim_token_ext_id, extId=node_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching node by claim token",
        )


def get_patched_image(module, api_instance, ext_id):
    """
    This method will return a patched image info using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Patched images api instance
        ext_id (str): External id of the patched image
    Returns:
        patched_image (object): Patched image info object (with etag headers)
    """
    try:
        return api_instance.get_patched_image_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching patched image with ext_id: {0}".format(
                ext_id
            ),
        )
