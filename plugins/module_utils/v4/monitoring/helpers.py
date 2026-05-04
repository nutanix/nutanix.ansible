# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_sda_policy(module, api_instance, ext_id):
    """
    Fetch a single System-Defined Alert Policy by its external ID.

    Args:
        module: Ansible module instance.
        api_instance: SystemDefinedPoliciesApi instance from ntnx_monitoring_py_client.
        ext_id (str): Unique external ID of the SDA policy.

    Returns:
        object: The SDA policy data object.
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system defined policy using ext_id",
        )
