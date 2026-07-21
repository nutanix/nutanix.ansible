# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_recommendation(module, api_instance, file_server_ext_id, ext_id):
    """
    This method will return file server recommendation info using its ext_id.
    Args:
        module: Ansible module
        api_instance: RecommendationsApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): external ID of the file server
        ext_id (str): recommendation external ID
    return:
        info (object): recommendation info
    """
    try:
        return api_instance.get_recommendation_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recommendation info using ext_id",
        )
