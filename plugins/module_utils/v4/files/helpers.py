# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_file_server(module, api_instance, ext_id):
    """
    Return the file server object identified by ``ext_id``.

    This is commonly used by DNS-record modules to validate that the target
    file server exists before invoking a write operation, and to obtain the
    ETag of the file server for optimistic concurrency control.

    Args:
        module (AnsibleModule): The Ansible module instance.
        api_instance: A ``ntnx_files_py_client.FileServersApi`` instance.
        ext_id (str): External identifier of the file server.

    Returns:
        object: The file server object (``.data``) returned by the SDK.
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
    List DNS records associated with a specific Nutanix Files file server.

    Any additional keyword arguments are forwarded to the SDK call and can
    be used for pagination / filtering (``_page``, ``_limit``, ``_filter``,
    ``_orderby``, ``_select``).

    Args:
        module (AnsibleModule): The Ansible module instance.
        api_instance: A ``ntnx_files_py_client.DnsApi`` instance.
        file_server_ext_id (str): External identifier of the parent file
            server whose DNS records should be listed.

    Returns:
        object: The raw ``ListDnsRecordsApiResponse`` SDK object.
    """
    try:
        return api_instance.list_dns_records(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing DNS records for file server",
        )
