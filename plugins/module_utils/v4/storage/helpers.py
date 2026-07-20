# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch a Volume Group by ext_id using the storage SDK.

    Args:
        module: Ansible module.
        api_instance: ``VolumeGroupApi`` from ``ntnx_storage_py_client``.
        ext_id: External ID of the Volume Group.

    Returns:
        The ``VolumeGroup`` model object.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Group info using ext_id",
        )
