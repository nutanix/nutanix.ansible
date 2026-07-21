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
    x_next_page_token=None,
):
    """
    Fetch a SnapshotChangedContent by its external ID.

    Args:
        module (AnsibleModule): The Ansible module instance.
        api_instance (SnapshotChangedContentsApi): SDK API instance.
        file_server_ext_id (str): External ID of the file server.
        mount_target_ext_id (str): External ID of the mount target.
        ext_id (str): External ID of the SnapshotChangedContent resource.
        x_next_page_token (str): Optional pagination token forwarded to the SDK.

    Returns:
        SnapshotChangedContent SDK data object.
    """
    try:
        resp = api_instance.get_snapshot_changed_content_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
            X_Next_Page_Token=x_next_page_token,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching snapshot changed content "
                "with ext_id '{0}' on file server '{1}' and mount target '{2}'"
            ).format(ext_id, file_server_ext_id, mount_target_ext_id),
        )
    return resp.data
