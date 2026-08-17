# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_data_stores_by_cluster(module, api_instance, cluster_ext_id, _filter=None):
    """
    Fetch the list of Data Stores for a given cluster.

    The DataStore list API is scoped to a cluster: it returns every
    Storage Container that is currently mounted on that cluster as a
    Data Store (each entry carries the container ext_id, container name,
    host ext_id / IP, capacity and free-space, and the list of VM names
    that live on that data store).

    Args:
        module: Ansible module.
        api_instance: StorageContainerApi instance from ntnx_storage_py_client.
        cluster_ext_id (str): Prism Element cluster external ID.
        _filter (str | None): Optional OData filter (e.g. "containerExtId eq '...'").

    Returns:
        object: DataStoreResponse SDK object.
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
            msg="Api Exception raised while fetching Data Stores for cluster",
        )


def find_data_store(
    module,
    api_instance,
    cluster_ext_id,
    container_ext_id=None,
    datastore_name=None,
    strict=True,
):
    """
    Locate a specific Data Store on a cluster by container ext_id or by
    datastore name. Returns the matching DataStore dict or None.

    Args:
        module: Ansible module.
        api_instance: StorageContainerApi instance.
        cluster_ext_id (str): Prism Element cluster external ID.
        container_ext_id (str | None): Storage container ext_id to match.
        datastore_name (str | None): Datastore name to match.
        strict (bool): If True, propagate list-API errors via module.fail_json
            (matches the historical helper behaviour). If False, return None
            on error so callers can treat a missing/404 list API as
            "no existing Data Store found" — used for idempotency checks.

    Returns:
        dict | None: matching DataStore as a dict, or None if not found.
    """
    if strict:
        resp = get_data_stores_by_cluster(module, api_instance, cluster_ext_id)
    else:
        try:
            resp = api_instance.get_data_stores(clusterExtId=cluster_ext_id)
        except Exception:
            return None
    data = getattr(resp, "data", None) or []
    for entry in data:
        entry_dict = entry.to_dict() if hasattr(entry, "to_dict") else entry
        if container_ext_id and entry_dict.get("container_ext_id") == container_ext_id:
            return entry_dict
        if datastore_name and entry_dict.get("datastore_name") == datastore_name:
            return entry_dict
    return None
