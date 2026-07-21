# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_object_store_profile(module, api_instance, file_server_ext_id, ext_id):
    """
    This method will return an object store profile using its external ID.
    Args:
        module: Ansible module
        api_instance: TierApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): external ID of the parent file server
        ext_id (str): object store profile external ID
    return:
        object_store_profile (object): object store profile info
    """
    try:
        return api_instance.get_object_store_profile_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store profile using ext_id",
        )
