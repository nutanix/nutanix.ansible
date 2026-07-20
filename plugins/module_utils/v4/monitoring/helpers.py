# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_sda_policy(module, api_instance, ext_id):
    """
    Fetch a single System-Defined Alert Policy by its external ID.

    Args:
        module: Ansible module
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client
        ext_id (str): SDA policy external ID
    Returns:
        info (object): SystemDefinedPolicy info object
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SDA policy info using ext_id",
        )


def get_cluster_config(
    module, api_instance, system_defined_policy_ext_id, cluster_ext_id
):
    """
    Fetch the cluster-specific configuration of an SDA policy for a cluster.

    Args:
        module: Ansible module
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client
        system_defined_policy_ext_id (str): SDA policy external ID
        cluster_ext_id (str): Cluster UUID (the ClusterConfig ext_id)
    Returns:
        info (object): ClusterConfig info object
    """
    try:
        return api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
            extId=cluster_ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching cluster config for SDA policy"
                " '{0}' and cluster '{1}'".format(
                    system_defined_policy_ext_id, cluster_ext_id
                )
            ),
        )


def get_cluster_config_with_etag(
    module, api_instance, system_defined_policy_ext_id, cluster_ext_id
):
    """
    Fetch the cluster-specific configuration of an SDA policy for a cluster and
    return both the data object and the raw API response (used to compute ETag).

    Args:
        module: Ansible module
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client
        system_defined_policy_ext_id (str): SDA policy external ID
        cluster_ext_id (str): Cluster UUID
    Returns:
        (raw_response, info): Tuple of raw API response and ClusterConfig data
    """
    try:
        resp = api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
            extId=cluster_ext_id,
        )
        return resp, resp.data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching cluster config for SDA policy"
                " '{0}' and cluster '{1}'".format(
                    system_defined_policy_ext_id, cluster_ext_id
                )
            ),
        )
