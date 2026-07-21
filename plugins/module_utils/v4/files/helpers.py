# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_infected_file(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch a single infected file by its external ID under a file server.

    Args:
        module: Ansible module object.
        api_instance: ``InfectedFilesApi`` from ``ntnx_files_py_client``.
        file_server_ext_id (str): External ID of the parent file server.
        ext_id (str): External ID of the infected file.

    Returns:
        InfectedFile SDK model instance.
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
                "using file_server_ext_id={0} and ext_id={1}".format(
                    file_server_ext_id, ext_id
                )
            ),
        )
