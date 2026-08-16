# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_volume_group(module, api_instance, ext_id):
    """
    Get volume group by ext_id
    Args:
        module: Ansible module
        api_instance: VolumeGroupApi instance from ntnx_volumes_py_client sdk
        ext_id: ext_id of volume group
    Returns:
        vg (obj): VolumeGroup info object
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume group info using ext_id",
        )


def list_external_iscsi_attachments(
    module, api_instance, volume_group_ext_id, **kwargs
):
    """
    List all external iSCSI attachments (iSCSI clients) associated with the
    given Volume Group.

    Args:
        module: Ansible module
        api_instance: VolumeGroupsApi instance from ntnx_volumes_py_client sdk
        volume_group_ext_id: ext_id of the Volume Group
        kwargs: Optional OData query parameters (``_page``, ``_limit``,
            ``_filter``, ``_orderby``, ``_expand``, ``_select``) supported by
            the SDK's ``list_external_iscsi_attachments_by_volume_group_id``.
    Returns:
        resp (obj): ListExternalIscsiAttachmentsApiResponse object
    """
    try:
        return api_instance.list_external_iscsi_attachments_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while listing external iSCSI attachments "
                "for Volume Group {0}"
            ).format(volume_group_ext_id),
        )


def get_external_iscsi_attachment_by_ext_id(
    module, api_instance, volume_group_ext_id, ext_id
):
    """
    Fetch a specific external iSCSI attachment by iterating the list of
    external attachments on the Volume Group.

    The Nutanix Volumes v4 API does not expose a GET-by-id endpoint for the
    external iSCSI attachment collection under a Volume Group; this helper
    filters the list response for the requested ``ext_id``.

    Args:
        module: Ansible module
        api_instance: VolumeGroupsApi instance from ntnx_volumes_py_client sdk
        volume_group_ext_id: ext_id of the Volume Group
        ext_id: ext_id of the external iSCSI attachment
    Returns:
        entity (obj): The matching attachment entity, or None if not found.
    """
    resp = list_external_iscsi_attachments(module, api_instance, volume_group_ext_id)
    data = getattr(resp, "data", None) or []
    for item in data:
        if getattr(item, "ext_id", None) == ext_id:
            return item
    return None
