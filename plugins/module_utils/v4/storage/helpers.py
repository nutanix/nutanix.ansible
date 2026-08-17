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


def get_data_stores_by_cluster(module, api_instance, cluster_ext_id, _filter=None):
    """
    List Data Stores available on a given cluster.

    Args:
        module: Ansible module.
        api_instance: ``StorageContainerApi`` instance from the storage SDK.
        cluster_ext_id (str): Cluster external ID.
        _filter (str): Optional OData filter expression.

    Returns:
        DataStoreResponse: raw SDK response object.
    """
    try:
        kwargs = {}
        if _filter:
            kwargs["_filter"] = _filter
        return api_instance.get_data_stores(clusterExtId=cluster_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=("Api Exception raised while fetching Data Stores for cluster ext_id"),
        )


def find_data_store(
    module,
    api_instance,
    cluster_ext_id,
    datastore_name=None,
    container_ext_id=None,
    ext_id=None,
):
    """
    Look up a single Data Store on the given cluster matching the supplied
    identifiers. Used for idempotency checks because the storage SDK does
    not expose a ``get_data_store_by_ext_id`` endpoint.

    Args:
        module: Ansible module.
        api_instance: ``StorageContainerApi`` instance.
        cluster_ext_id (str): Cluster external ID.
        datastore_name (str): Optional Data Store name to match.
        container_ext_id (str): Optional container ext_id to match.
        ext_id (str): Optional Data Store ext_id to match.

    Returns:
        DataStore | None: matching Data Store object, or ``None`` if not found.
    """
    _filter = None
    if container_ext_id:
        _filter = "containerExtId eq '{0}'".format(container_ext_id)
    resp = get_data_stores_by_cluster(
        module, api_instance, cluster_ext_id, _filter=_filter
    )
    data = getattr(resp, "data", None) or []
    for item in data:
        if ext_id and getattr(item, "ext_id", None) == ext_id:
            return item
        if datastore_name and getattr(item, "datastore_name", None) == datastore_name:
            if (
                container_ext_id
                and getattr(item, "container_ext_id", None) != container_ext_id
            ):
                continue
            return item
    return None
