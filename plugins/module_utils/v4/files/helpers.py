# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_snapshot_schedule(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch a snapshot schedule for a file server by its ext_id.

    Args:
        module: Ansible module.
        api_instance: SnapshotSchedulesApi instance from ntnx_files_py_client sdk.
        file_server_ext_id (str): External ID of the parent file server.
        ext_id (str): Snapshot schedule external ID.
    Returns:
        object: Snapshot schedule info.
    """
    try:
        return api_instance.get_snapshot_schedule_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snapshot schedule info using ext_id",
        )
