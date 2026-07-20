# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch a Volume Group by its external ID via the storage v4 API.

    Args:
        module (AnsibleModule): The Ansible module object.
        api_instance (ntnx_storage_py_client.VolumeGroupApi): SDK API instance.
        ext_id (str): External ID of the Volume Group.

    Returns:
        object: The Volume Group data model returned by the SDK.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Group info using ext_id",
        )


def get_external_attachments(module, api_instance, volume_group_ext_id, **kwargs):
    """
    Fetch the list of external (iSCSI) attachments for a Volume Group.

    Args:
        module (AnsibleModule): The Ansible module object.
        api_instance (ntnx_storage_py_client.VolumeGroupApi): SDK API instance.
        volume_group_ext_id (str): External ID of the parent Volume Group.
        **kwargs: OData query args (_page, _limit, _filter, _orderby, _expand).

    Returns:
        object: The GetExternalAttachmentsApiResponse from the SDK.
    """
    try:
        return api_instance.get_external_attachments(
            extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching external attachments for Volume Group",
        )


def get_external_attachment_by_ext_id(
    module, api_instance, volume_group_ext_id, ext_id
):
    """
    Look up a single external attachment by its ``ext_id`` inside the
    given Volume Group.

    The storage v4 API has no dedicated get-by-id endpoint for
    ``ExternalAttachment``, so this helper fetches the list of external
    attachments for the Volume Group and returns the entry whose
    ``ext_id`` matches. Returns ``None`` if not found.

    Args:
        module (AnsibleModule): The Ansible module object.
        api_instance (ntnx_storage_py_client.VolumeGroupApi): SDK API instance.
        volume_group_ext_id (str): External ID of the parent Volume Group.
        ext_id (str): External ID of the iSCSI client attachment to look up.

    Returns:
        object | None: The matching attachment object, or None if not found.
    """
    resp = get_external_attachments(
        module, api_instance, volume_group_ext_id, _limit=100
    )
    attachments = getattr(resp, "data", None) or []
    for attachment in attachments:
        if getattr(attachment, "ext_id", None) == ext_id:
            return attachment
    return None
