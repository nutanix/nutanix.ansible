# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_iscsi_client(module, api_instance, ext_id):
    """
    Return an IscsiClient info object by ext_id.

    Args:
        module: Ansible module.
        api_instance: IscsiClientApi instance from ntnx_storage_py_client.
        ext_id: External ID of the iSCSI client.

    Returns:
        IscsiClient info object (unwrapped from the API response).
    """
    try:
        return api_instance.get_iscsi_client_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching iSCSI client info using ext_id",
        )
