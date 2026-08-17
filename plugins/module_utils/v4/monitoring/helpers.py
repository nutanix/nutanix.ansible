# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_sda_policy(module, api_instance, ext_id):
    """
    Fetch a single System-Defined Alert (SDA) policy by external ID using
    ``SystemDefinedPoliciesApi.get_sda_policy_by_id``.
    Args:
        module (AnsibleModule): running Ansible module instance.
        api_instance (SystemDefinedPoliciesApi): monitoring SDK API handle.
        ext_id (str): unique external ID of the SDA policy.
    Returns:
        object: SDA policy data object from the SDK response.
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system defined alert policy using ext_id",
        )


def get_cluster_config(module, api_instance, sda_ext_id, ext_id):
    """
    Fetch the cluster-specific configuration of an SDA policy for a given
    cluster using ``SystemDefinedPoliciesApi.get_cluster_config_by_id``.
    Args:
        module (AnsibleModule): running Ansible module instance.
        api_instance (SystemDefinedPoliciesApi): monitoring SDK API handle.
        sda_ext_id (str): unique external ID of the SDA policy.
        ext_id (str): cluster UUID.
    Returns:
        object: ClusterConfig data object from the SDK response.
    """
    try:
        return api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=sda_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster config for SDA policy",
        )
