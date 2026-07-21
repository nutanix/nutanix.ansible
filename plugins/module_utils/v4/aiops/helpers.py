# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_simulation(module, api_instance, ext_id):
    """
    Fetch a single simulation by its external ID.

    Args:
        module (object): Ansible module object
        api_instance (object): aiops ScenariosApi instance
        ext_id (str): External ID of the simulation

    Returns:
        info (object): simulation info object
    """
    try:
        return api_instance.get_simulation_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching simulation info using ext_id",
        )
