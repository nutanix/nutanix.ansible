# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_infected_file(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch an infected file by its external ID within a given file server.

    Args:
        module (object): Ansible module object
        api_instance (object): InfectedFilesApi instance from ntnx_files_py_client SDK
        file_server_ext_id (str): The external identifier of the file server
        ext_id (str): The external identifier of the infected file
    Returns:
        info (object): infected file info
    """
    try:
        return api_instance.get_infected_file_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching infected file info "
                "using ext_id '{0}' on file server '{1}'".format(
                    ext_id, file_server_ext_id
                )
            ),
        )


def get_file_server(module, api_instance, ext_id):
    """
    Fetch a file server by its external ID.

    Args:
        module (object): Ansible module object
        api_instance (object): FileServersApi instance from ntnx_files_py_client SDK
        ext_id (str): The external identifier of the file server
    Returns:
        info (object): file server info
    """
    try:
        return api_instance.get_file_server_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server info using ext_id",
        )
