# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_object_store(module, object_stores_api, ext_id):
    """
    This method will return object store info using external ID.
    Args:
        module: Ansible module
        object_stores_api: ObjectStoresApi instance from ntnx_objects_py_client sdk
        ext_id (str): object store external ID
    return:
        object_store_info (object): object store info
    """
    try:
        return object_stores_api.get_objectstore_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store info using ext_id",
        )


def get_object_store_certificate(
    module, object_stores_api, ext_id, object_store_ext_id
):
    """
    This method will return object store certificate info using external ID.
    Args:
        module: Ansible module
        object_stores_api: ObjectStoresApi instance from ntnx_objects_py_client sdk
        ext_id (str): object store certificate external ID
        object_store_ext_id (str): object store external ID
    return:
        object_store_info (object): object store info
    """
    try:
        return object_stores_api.get_certificate_by_id(
            extId=ext_id, objectStoreExtId=object_store_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store certificate info using ext_id",
        )
