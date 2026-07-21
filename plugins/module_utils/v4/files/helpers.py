# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_snapshot_changed_content(
    module,
    api_instance,
    file_server_ext_id,
    mount_target_ext_id,
    ext_id,
    next_page_token=None,
):
    """
    Fetch a SnapshotChangedContent bucket by external identifier.

    Args:
        module (object): Ansible module object.
        api_instance (object): SnapshotChangedContentsApi instance.
        file_server_ext_id (str): The file server external identifier.
        mount_target_ext_id (str): The mount target external identifier.
        ext_id (str): The SnapshotChangedContent bucket external identifier.
        next_page_token (str): Optional pagination continuation token
            returned as ``X-Next-Page-Token`` header by a previous call.

    Returns:
        info (object): SnapshotChangedContent detail object (``resp.data``).
    """
    try:
        return api_instance.get_snapshot_changed_content_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
            X_Next_Page_Token=next_page_token,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snapshot changed content info using ext_id",
        )
