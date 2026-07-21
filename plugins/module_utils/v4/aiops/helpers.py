# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_scenario(module, api_instance, ext_id):
    """
    Fetch a single capacity planning scenario by its ext_id.

    Args:
        module: Ansible module.
        api_instance: ScenariosApi instance from ntnx_aiops_py_client.
        ext_id (str): UUID of the scenario.

    Returns:
        scenario (object): Scenario info object.
    """
    try:
        return api_instance.get_scenario_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching capacity planning scenario using ext_id",
        )


def get_scenario_report(module, api_instance, scenario_ext_id):
    """
    Fetch the generated report for a capacity planning scenario.

    Args:
        module: Ansible module.
        api_instance: ScenariosApi instance from ntnx_aiops_py_client.
        scenario_ext_id (str): UUID of the scenario whose report should be fetched.

    Returns:
        report (object): Report response data.
    """
    try:
        return api_instance.get_scenario_report(scenarioExtId=scenario_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching scenario report using scenario ext_id",
        )
