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


def get_object_store_certificate_authority(
    module, object_stores_api, ext_id, object_store_ext_id
):
    """
    This method will return the certificate authority (CA) of an object store
    certificate using external ID.
    Args:
        module: Ansible module
        object_stores_api: ObjectStoresApi instance from ntnx_objects_py_client sdk
        ext_id (str): object store certificate external ID
        object_store_ext_id (str): object store external ID
    return:
        ca_response (object): GetCaApiResponse instance
    """
    try:
        return object_stores_api.get_ca_by_certificate_id(
            certificateExtId=ext_id, objectStoreExtId=object_store_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store certificate authority using ext_id",
        )


def get_bucket(module, buckets_api, object_store_ext_id, bucket_name, **kwargs):
    """
    This method will return bucket info using object store ext ID and bucket name.
    Args:
        module: Ansible module
        buckets_api: BucketsApi instance from ntnx_objects_py_client sdk
        object_store_ext_id (str): object store external ID
        bucket_name (str): bucket name
        kwargs: optional kwargs (for example x_ntnx_objects_namespace)
    return:
        bucket_info (object): bucket info
    """
    try:
        return buckets_api.get_bucket_by_name(
            objectStoreExtId=object_store_ext_id, bucketName=bucket_name, **kwargs
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store bucket info",
        )


def get_data_movement_target(
    module, data_movement_targets_api, object_store_ext_id, ext_id
):
    """
    This method will return data movement target info using external ID.
    Args:
        module: Ansible module
        data_movement_targets_api: DataMovementTargetsApi instance
        object_store_ext_id (str): object store external ID
        ext_id (str): data movement target external ID
    return:
        data_movement_target_info (object): data movement target info
    """
    try:
        return data_movement_targets_api.get_data_movement_target_by_id(
            objectStoreExtId=object_store_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store data movement target info using ext_id",
        )


def get_storage_backend(module, storage_backends_api, object_store_ext_id, ext_id):
    """
    This method will return storage backend info using external ID.
    Args:
        module: Ansible module
        storage_backends_api: StorageBackendsApi instance
        object_store_ext_id (str): object store external ID
        ext_id (str): storage backend external ID
    return:
        storage_backend_info (object): storage backend info
    """
    try:
        return storage_backends_api.get_storage_backend_by_id(
            objectStoreExtId=object_store_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store storage backend info using ext_id",
        )
