# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_volume_group_metadata_info(module, api_instance, ext_id):
    """
    Fetch the metadata information associated with a Volume Group.

    Wraps the storage SDK ``get_volume_group_metadata_info`` call, converts
    any raised SDK exception into a descriptive ``module.fail_json`` via
    :func:`raise_api_exception`, and returns the raw API response so callers
    can inspect ``resp.data`` and read the response's ETag when they need to
    chain an update.

    Args:
        module: Ansible module instance (used for error reporting).
        api_instance: ntnx_storage_py_client ``VolumeGroupApi`` instance.
        ext_id (str): The external identifier of the Volume Group whose
            metadata information should be returned.

    Returns:
        ntnx_storage_py_client.GetVolumeGroupMetadataInfoApiResponse: The full
        API response envelope. Callers typically read ``response.data`` for
        the Metadata payload.
    """
    try:
        return api_instance.get_volume_group_metadata_info(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching Volume Group Metadata Info "
                "using ext_id: {0}".format(ext_id)
            ),
        )
