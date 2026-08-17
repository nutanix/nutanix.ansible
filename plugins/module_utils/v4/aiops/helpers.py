# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_scenario_report(module, api_instance, scenario_ext_id):
    """
    Download the generated capacity planning report for a scenario.

    The AIOps SDK returns a local filesystem ``Path`` pointing to the
    downloaded PDF report. Callers are responsible for consuming that
    path (moving/reading/uploading) as needed.

    Args:
        module (AnsibleModule): The Ansible module object.
        api_instance (ScenariosApi): The AIOps ScenariosApi instance.
        scenario_ext_id (str): The external ID of the capacity planning scenario.

    Returns:
        pathlib.Path | object: The downloaded report file path (on success) or
        an SDK error object; may be ``None`` if the server returned no body.
    """
    try:
        return api_instance.get_scenario_report(scenarioExtId=scenario_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching scenario report using scenario ext_id",
        )
