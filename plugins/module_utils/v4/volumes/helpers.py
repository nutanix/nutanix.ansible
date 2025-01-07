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
