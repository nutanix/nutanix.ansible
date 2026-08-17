# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch a Volume Group by its external ID using the storage v4 SDK.

    Args:
        module: Ansible module.
        api_instance: ntnx_storage_py_client.VolumeGroupApi instance.
        ext_id (str): External identifier of the Volume Group.

    Returns:
        VolumeGroup: SDK response ``data`` object for the Volume Group.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching Volume Group info "
                "using ext_id: {0}".format(ext_id)
            ),
        )
