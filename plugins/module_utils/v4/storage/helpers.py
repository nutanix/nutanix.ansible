# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_volume_disk(module, api_instance, volume_group_ext_id, ext_id):
    """
    Fetch a single Volume Disk associated with a Volume Group.

    Args:
        module (AnsibleModule): The Ansible module currently running.
        api_instance (ntnx_storage_py_client.VolumeGroupApi): API stub built
            from ``get_vg_api_instance``.
        volume_group_ext_id (str): Volume Group external identifier that
            owns the disk.
        ext_id (str): External identifier of the Volume Disk to fetch.

    Returns:
        object: The Volume Disk data (``resp.data``) returned by the SDK.

    Raises:
        Fails the module via ``raise_api_exception`` on any SDK failure so
        that callers do not have to duplicate error handling.
    """
    try:
        return api_instance.get_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Disk info using ext_id",
        )
