# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_cluster_config(module, api_instance, sda_policy_ext_id, ext_id):
    """
    Fetch a single ClusterConfig for a given SDA policy and cluster.

    Args:
        module: Ansible module.
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client.
        sda_policy_ext_id (str): The System-Defined Alert policy external ID.
        ext_id (str): The cluster external ID (also acts as ClusterConfig ext_id).

    Returns:
        info (object): ClusterConfig response object (with etag reserved metadata).
    """
    try:
        return api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=sda_policy_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster config using ext_id",
        )


def get_sda_policy(module, api_instance, ext_id):
    """
    Fetch a single System-Defined Alert policy by ext_id.

    Args:
        module: Ansible module.
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client.
        ext_id (str): SDA policy external ID.

    Returns:
        info (object): SystemDefinedPolicy response object.
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SDA policy using ext_id",
        )
