# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_scenario(module, api_instance, ext_id):
    """
    Get a capacity planning scenario by ext_id.

    The runway payload for a scenario is refreshed asynchronously by the
    GenerateRunway action; callers use this helper to fetch the updated
    scenario after the runway task completes.

    Args:
        module: Ansible module.
        api_instance: ntnx_aiops_py_client.ScenariosApi instance.
        ext_id: External ID (UUID) of the capacity planning scenario.

    Returns:
        Scenario data object from the SDK.
    """
    try:
        return api_instance.get_scenario_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching capacity planning scenario using ext_id",
        )
