# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_global_report_setting(module, api_instance, user_ext_id):
    """
    Fetch the GlobalReportSetting for the specified user.

    ``GlobalReportSetting`` is a per-user singleton — the reporting service
    always returns the setting associated with ``user_ext_id``. On failure
    this helper delegates to :func:`raise_api_exception` which calls
    ``module.fail_json`` with a descriptive message and the underlying SDK
    error body.

    Args:
        module (AnsibleModule): The Ansible module (used for error reporting).
        api_instance: A ``GlobalReportSettingApi`` instance built via
            :func:`get_global_report_setting_api_instance`.
        user_ext_id (str): External ID of the user whose global report setting
            should be fetched. Passed as the ``userExtId`` path parameter.

    Returns:
        The raw :class:`GetGlobalReportSettingApiResponse` object returned by
        the SDK. Callers typically read ``resp.data`` for the entity itself
        and use ``get_etag(resp.data)`` to pick up the concurrency token for
        subsequent updates.
    """
    try:
        return api_instance.get_global_report_setting(userExtId=user_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching global report setting "
                "for user ext_id"
            ),
        )
