# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_quota_policy(
    module, api_instance, file_server_ext_id, mount_target_ext_id, ext_id
):
    """
    This method will return quota policy info using its ext_id.
    Args:
        module (object): Ansible module object
        api_instance (object): QuotaPoliciesApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): external ID of the file server
        mount_target_ext_id (str): external ID of the mount target
        ext_id (str): quota policy external ID
    return:
        info (object): quota policy info
    """
    try:
        return api_instance.get_quota_policy_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching quota policy info using ext_id",
        )
