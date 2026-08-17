# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_alert_email_configuration(module, api_instance):
    """
    This method will return alert email configuration info (singleton).
    Args:
        module: Ansible module
        api_instance: AlertEmailConfigurationApi instance from
            ntnx_monitoring_py_client sdk
    return:
        info (object): alert email configuration info object
    """
    try:
        return api_instance.get_alert_email_configuration().data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alert email configuration info",
        )
