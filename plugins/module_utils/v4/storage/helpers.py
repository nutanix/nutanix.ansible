# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch Volume Group by ext_id using the storage v4 SDK.
    Args:
        module: Ansible module
        api_instance: VolumeGroupApi instance from ntnx_storage_py_client SDK
        ext_id: ext_id of the Volume Group
    Returns:
        The VolumeGroup data object.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Group info using ext_id",
        )


def get_vm_attachments(module, api_instance, volume_group_ext_id, **kwargs):
    """
    Fetch all VM attachments for a Volume Group using the storage v4 SDK.
    Args:
        module: Ansible module
        api_instance: VolumeGroupApi instance from ntnx_storage_py_client SDK
        volume_group_ext_id: ext_id of the Volume Group
        kwargs: Optional pagination arguments (``_page``, ``_limit``).
    Returns:
        The GetVmAttachmentsApiResponse response object.
    """
    try:
        return api_instance.get_vm_attachments(extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM attachments for Volume Group",
        )


def find_vm_attachment(module, api_instance, volume_group_ext_id, vm_ext_id):
    """
    Return the specific VmAttachment for the given VM ext_id under a Volume Group.

    Uses paginated ``get_vm_attachments`` to iterate over all attachments
    associated with the Volume Group and return the entry whose ``ext_id``
    matches the VM ext_id. Returns ``None`` if no such attachment exists.

    Args:
        module: Ansible module.
        api_instance: VolumeGroupApi instance from ntnx_storage_py_client SDK.
        volume_group_ext_id: ext_id of the Volume Group.
        vm_ext_id: ext_id of the VM whose attachment is to be found.
    """
    page = 0
    limit = 100
    while True:
        resp = get_vm_attachments(
            module,
            api_instance,
            volume_group_ext_id,
            _page=page,
            _limit=limit,
        )
        data = getattr(resp, "data", None) or []
        for attachment in data:
            if getattr(attachment, "ext_id", None) == vm_ext_id:
                return attachment
        if len(data) < limit:
            return None
        page += 1
