# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_file_server(module, api_instance, ext_id):
    """
    Fetch a Nutanix Files file server by its external ID.

    Args:
        module (object): Ansible module object
        api_instance (object): FileServersApi instance from ntnx_files_py_client
        ext_id (str): external identifier of the file server

    Returns:
        info (object): file server data object
    """
    try:
        return api_instance.get_file_server_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server info using ext_id",
        )


def list_dns_records(module, api_instance, file_server_ext_id, **kwargs):
    """
    Fetch the list of DNS records for a file server.

    Args:
        module (object): Ansible module object
        api_instance (object): DnsApi instance from ntnx_files_py_client
        file_server_ext_id (str): external identifier of the file server
        kwargs (dict): Optional keyword arguments forwarded to
            ``list_dns_records`` (``_page``, ``_limit``, ``_filter``,
            ``_orderby``, ``_select``)

    Returns:
        resp (object): ListDnsRecordsApiResponse object
    """
    try:
        return api_instance.list_dns_records(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching DNS records for file server",
        )


def get_dns_record(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch a specific DNS record for a file server by its external ID.

    The Nutanix Files v4 SDK does not expose a ``get_dns_record_by_id``
    endpoint, so this helper lists all DNS records for the given file
    server and filters by ``extId``.

    Args:
        module (object): Ansible module object
        api_instance (object): DnsApi instance from ntnx_files_py_client
        file_server_ext_id (str): external identifier of the file server
        ext_id (str): external identifier of the DNS record

    Returns:
        record (object): matching DNS record data object, or None if
            no record with the given ext_id was found
    """
    resp = list_dns_records(module, api_instance, file_server_ext_id)
    records = getattr(resp, "data", None) or []
    for record in records:
        if getattr(record, "ext_id", None) == ext_id:
            return record
    return None
