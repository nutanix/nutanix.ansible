# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_alert(module, api_instance, ext_id):
    """
    Fetch a single alert by its external ID.

    Args:
        module (object): Ansible module object.
        api_instance (object): ``AlertsApi`` instance from
            ``ntnx_monitoring_py_client``.
        ext_id (str): External ID of the alert.

    Returns:
        object: Alert info wrapper (includes ETag headers on the response).
    """
    try:
        return api_instance.get_alert_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alert info using ext_id",
        )
