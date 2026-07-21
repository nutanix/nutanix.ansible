# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_mount_target_stats(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch statistics for a specific Nutanix Files mount target.

    The mount target statistics datasource requires the parent file server
    external ID, the mount target external ID and a reporting time window
    (start_time and end_time). The sampling interval and stat type are
    optional down-sampling controls read from the module parameters.

    Args:
        module (AnsibleModule): AnsibleModule instance.
        api_instance (AnalyticsApi): files analytics api instance.
        file_server_ext_id (str): external ID of the parent file server.
        ext_id (str): external ID of the mount target.
    Returns:
        MountTargetStatsApiResponse: the raw SDK response object.
    """
    try:
        resp = api_instance.get_mount_target_stats(
            fileServerExtId=file_server_ext_id,
            extId=ext_id,
            _startTime=module.params.get("start_time"),
            _endTime=module.params.get("end_time"),
            _samplingInterval=module.params.get("sampling_interval"),
            _statType=module.params.get("stat_type"),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching mount target stats for "
                "mount target ext_id: {0} on file server ext_id: {1}".format(
                    ext_id, file_server_ext_id
                )
            ),
        )
    return resp
