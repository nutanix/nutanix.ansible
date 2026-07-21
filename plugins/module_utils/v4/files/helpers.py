# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_notification_policy(module, api_instance, ext_id, file_server_ext_id):
    """
    This method will return a notification policy using its ext_id.
    Args:
        module: Ansible module
        api_instance: NotificationPoliciesApi instance from ntnx_files_py_client sdk
        ext_id (str): notification policy external ID
        file_server_ext_id (str): file server external ID that owns the policy
    return:
        info (object): notification policy info
    """
    try:
        return api_instance.get_notification_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching notification policy info using ext_id",
        )
