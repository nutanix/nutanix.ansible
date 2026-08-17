# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_file_server(module, api_instance, ext_id):
    """
    Get file server by ext_id.
    Args:
        module: Ansible module
        api_instance: FileServersApi instance from ntnx_files_py_client sdk
        ext_id: ext_id of the file server
    Returns:
        file_server (obj): file server info object
    """
    try:
        return api_instance.get_file_server_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server info using ext_id",
        )


def normalize_response_data(data):
    """
    Normalize the ``data`` field of a v4 API response into a JSON-serializable
    structure.

    Some action endpoints (for example, recalculate cold data) return a
    ``OneOf`` payload that may resolve to a single SDK model object, a list of
    application messages, an empty list, or an empty map. This helper converts
    any of those shapes into plain dicts/lists so they can be returned as
    module output.

    Args:
        data (object): The ``data`` attribute of a v4 SDK API response.
    Returns:
        The normalized data as a dict, list, or None.
    """
    if data is None:
        return None
    if isinstance(data, list):
        return [item.to_dict() if hasattr(item, "to_dict") else item for item in data]
    if hasattr(data, "to_dict"):
        return data.to_dict()
    return data
