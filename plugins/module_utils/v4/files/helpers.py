# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_file_server_stats(module, analytics_api, ext_id, **kwargs):
    """
    Retrieve statistics for a file server identified by ``ext_id``.

    Args:
        module (AnsibleModule): the running Ansible module instance.
        analytics_api: AnalyticsApi instance from ntnx_files_py_client.
        ext_id (str): file server external identifier.
        **kwargs: additional query params passed through to the SDK call
            (e.g. ``_startTime``, ``_endTime``, ``_samplingInterval``,
            ``_statType``, ``_select``).

    Returns:
        SDK response object for the file server stats API.
    """
    try:
        resp = analytics_api.get_file_server_stats(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server stats for ext_id: {0}".format(
                ext_id
            ),
        )
    return resp


def get_antivirus_server_stats(
    module, analytics_api, file_server_ext_id, ext_id, **kwargs
):
    """
    Retrieve statistics for an antivirus server attached to a file server.

    Args:
        module (AnsibleModule): the running Ansible module instance.
        analytics_api: AnalyticsApi instance from ntnx_files_py_client.
        file_server_ext_id (str): external id of the parent file server.
        ext_id (str): external id of the antivirus server.
        **kwargs: additional query params passed through to the SDK call.

    Returns:
        SDK response object for the antivirus server stats API.
    """
    try:
        resp = analytics_api.get_antivirus_server_stats(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching antivirus server stats for ext_id: {0}".format(
                ext_id
            ),
        )
    return resp


def get_mount_target_stats(module, analytics_api, file_server_ext_id, ext_id, **kwargs):
    """
    Retrieve statistics for a mount target attached to a file server.

    Args:
        module (AnsibleModule): the running Ansible module instance.
        analytics_api: AnalyticsApi instance from ntnx_files_py_client.
        file_server_ext_id (str): external id of the parent file server.
        ext_id (str): external id of the mount target.
        **kwargs: additional query params passed through to the SDK call.

    Returns:
        SDK response object for the mount target stats API.
    """
    try:
        resp = analytics_api.get_mount_target_stats(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching mount target stats for ext_id: {0}".format(
                ext_id
            ),
        )
    return resp
