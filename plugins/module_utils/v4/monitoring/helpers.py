# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_cluster_config_by_sda_id(
    module, api_instance, system_defined_policy_ext_id, ext_id
):
    """
    Fetch cluster-specific configuration associated with a System-Defined Alert
    Policy for a cluster.

    Args:
        module: Ansible module
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client sdk
        system_defined_policy_ext_id (str): Unique ID of the System-Defined Alert Policy
        ext_id (str): Cluster UUID

    Returns:
        cluster_config (object): ClusterConfig SDK object with etag headers preserved
    """
    try:
        return api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching cluster config for SDA policy "
                "ext_id: {0} and cluster ext_id: {1}".format(
                    system_defined_policy_ext_id, ext_id
                )
            ),
        )


def get_sda_policy_by_id(module, api_instance, ext_id):
    """
    Fetch a System-Defined Alert Policy by its external ID.

    Args:
        module: Ansible module
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client sdk
        ext_id (str): Unique ID of the System-Defined Alert Policy

    Returns:
        sda_policy (object): SystemDefinedPolicy SDK object
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching System-Defined Alert Policy "
                "info using ext_id: {0}".format(ext_id)
            ),
        )
