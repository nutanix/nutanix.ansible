# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_antivirus_server(module, api_instance, ext_id, file_server_ext_id):
    """
    This method will return antivirus server info using its ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): AntivirusServersApi instance from ntnx_files_py_client sdk
        ext_id (str): antivirus server external ID
        file_server_ext_id (str): external ID of the file server the antivirus server belongs to
    return:
        info (object): antivirus server info
    """
    try:
        return api_instance.get_antivirus_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching antivirus server info using ext_id",
        )
