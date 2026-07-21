# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_uda_policy(module, api_instance, ext_id):
    """
    Fetch a single User-Defined Alert (UDA) policy by its ext_id.

    Args:
        module: The Ansible module — used to surface API failures.
        api_instance: An instance of
            ``ntnx_monitoring_py_client.UserDefinedPoliciesApi``.
        ext_id (str): The external ID of the User-Defined Alert policy.

    Returns:
        object: The policy payload from ``data`` of the SDK response.
    """
    try:
        return api_instance.get_uda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching User-Defined Alert policy using ext_id",
        )
