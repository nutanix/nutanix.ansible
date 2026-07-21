# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_file_server(module, api_instance, ext_id):
    """
    Get a Nutanix Files file server by its external ID.
    Args:
        module: Ansible module
        api_instance: FileServersApi instance from ntnx_files_py_client sdk
        ext_id (str): file server external ID
    Returns:
        file_server (obj): file server info object
    """
    try:
        return api_instance.get_file_server_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server info using ext_id",
        )
