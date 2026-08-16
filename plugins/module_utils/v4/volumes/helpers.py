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


def get_volume_group_metadata(module, api_instance, volume_group_ext_id):
    """
    Get VolumeGroupMetadata for a Volume Group.

    The SDK method ``get_volume_group_metadata_by_id`` is a deprecated v4.2
    API that reads the ``owner_reference`` and ``category_ids`` metadata of
    a Volume Group. Newer clients should prefer ``get_volume_group_by_id``
    with the ``$expand=metadata`` OData query, but the endpoint is still
    served for backward compatibility.

    Args:
        module: Ansible module.
        api_instance: VolumeGroupsApi instance from ntnx_volumes_py_client.
        volume_group_ext_id: External ID of the parent Volume Group.

    Returns:
        VolumeGroupMetadata SDK model on success. Never returns ``None`` — on
        error it fails the module through ``raise_api_exception``.
    """
    try:
        return api_instance.get_volume_group_metadata_by_id(
            volumeGroupExtId=volume_group_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching Volume Group metadata for "
                "volume_group_ext_id={0}".format(volume_group_ext_id)
            ),
        )
