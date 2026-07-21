# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch a Volume Group object from the storage v4 API by its external ID.

    Args:
        module (object): Ansible module object.
        api_instance (object): ``VolumeGroupApi`` instance from
            ``ntnx_storage_py_client``.
        ext_id (str): Volume Group external ID.

    Returns:
        vg (object): ``VolumeGroup`` model object.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume group info using ext_id",
        )
