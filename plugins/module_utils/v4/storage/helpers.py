# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_storage_container(module, api_instance, ext_id):
    """
    Fetch a Storage Container using its external ID.

    Args:
        module: Ansible module.
        api_instance: StorageContainerApi instance from ``ntnx_storage_py_client``.
        ext_id (str): The Storage Container external ID.
    Returns:
        object: Storage Container SDK model (``resp.data``).
    """
    try:
        return api_instance.get_storage_container_by_ext_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage container info using ext_id",
        )
