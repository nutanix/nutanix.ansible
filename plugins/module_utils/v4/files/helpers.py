# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_mount_target(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch a single mount target by (fileServerExtId, extId).

    Args:
        module: Ansible module.
        api_instance: MountTargetsApi instance from ntnx_files_py_client sdk.
        file_server_ext_id (str): Parent file server external ID.
        ext_id (str): Mount target external ID.

    Returns:
        The MountTarget data object.
    """
    try:
        return api_instance.get_mount_target_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching mount target info using ext_id",
        )
