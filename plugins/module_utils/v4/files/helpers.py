# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_partner_server(module, api_instance, file_server_ext_id, ext_id):
    """
    This method will return partner server info using its ext_id.
    Args:
        module: Ansible module
        api_instance: PartnerServersApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): external ID of the file server
        ext_id (str): partner server external ID
    return:
        info (object): partner server info
    """
    try:
        return api_instance.get_partner_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching partner server info using ext_id",
        )


def get_partner_server_by_name(module, api_instance, file_server_ext_id, name):
    """
    This method will return partner server info using its name if it exists.
    It is used to support create idempotency and to resolve the external ID of a
    freshly created partner server when the task does not report it reliably.
    Args:
        module: Ansible module
        api_instance: PartnerServersApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): external ID of the file server
        name (str): partner server name
    return:
        info (object): partner server info if found, else None
    """
    try:
        resp = api_instance.list_partner_servers(
            fileServerExtId=file_server_ext_id,
            _filter="name eq '{0}'".format(name),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching partner server info using name",
        )
    partner_servers = getattr(resp, "data", None)
    if not partner_servers:
        return None
    return partner_servers[0]
