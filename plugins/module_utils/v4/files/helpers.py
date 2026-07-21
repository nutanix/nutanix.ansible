# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_antivirus_server_stats(
    module, api_instance, file_server_ext_id, ext_id, msg=None
):
    """
    Fetch antivirus server statistics for a single antivirus server on a
    file server for the requested time window.

    The Nutanix Files stats endpoint only exposes a get-by-id style read for
    antivirus server statistics, so both the stats module and the info module
    reuse this helper to avoid duplicating the fetch logic.

    Args:
        module (AnsibleModule): AnsibleModule instance. The time window and
            optional query parameters are read from ``module.params``.
        api_instance (AnalyticsApi): files AnalyticsApi instance.
        file_server_ext_id (str): external id of the file server.
        ext_id (str): external id of the antivirus server.
        msg (str): error message to surface if the API call fails.

    Returns:
        AntivirusServerStatsApiResponse: the raw SDK response.
    """
    if msg is None:
        msg = "Api Exception raised while fetching antivirus server stats"

    resp = None
    try:
        resp = api_instance.get_antivirus_server_stats(
            fileServerExtId=file_server_ext_id,
            extId=ext_id,
            _startTime=module.params.get("start_time"),
            _endTime=module.params.get("end_time"),
            _samplingInterval=module.params.get("sampling_interval"),
            _statType=module.params.get("stat_type"),
            _select=module.params.get("select"),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=msg,
        )
    return resp
