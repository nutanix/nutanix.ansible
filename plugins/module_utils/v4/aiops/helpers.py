# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_scenario(module, api_instance, ext_id):
    """
    Fetch a capacity planning scenario by its external ID.

    Args:
        module: Ansible module.
        api_instance: ScenariosApi instance from ntnx_aiops_py_client.
        ext_id (str): External ID of the capacity planning scenario.

    Returns:
        object: Scenario info object.
    """
    try:
        return api_instance.get_scenario_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching capacity planning scenario using ext_id",
        )
