# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_project(module, api_instance, ext_id):
    """
    Get project by ext_id.
    Args:
        module: Ansible module
        api_instance: ProjectsApi instance
        ext_id: External ID of the project
    Returns:
        Project data object
    """
    try:
        return api_instance.get_project_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching project using ext_id",
        )
