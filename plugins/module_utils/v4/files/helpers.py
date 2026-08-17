# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_email_config(module, api_instance, file_server_ext_id):
    """
    This method will fetch the email configuration of a file server.

    The email configuration is a singleton per file server, so it is fetched
    using the external identifier of the file server (not its own external ID).

    Args:
        module (object): Ansible module object
        api_instance (object): QuotaPoliciesApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): External identifier of the file server
    Returns:
        email_config (object): EmailConfig info object
    """
    try:
        return api_instance.get_email_config(fileServerExtId=file_server_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching email configuration for file server",
        )
