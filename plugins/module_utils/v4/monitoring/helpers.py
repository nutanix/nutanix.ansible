# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_event(module, api_instance, ext_id):
    """
    This method will return event info using its ext_id.
    Args:
        module: Ansible module object
        api_instance: EventsApi instance from ntnx_monitoring_py_client sdk
        ext_id (str): event external ID
    return:
        info (object): event info
    """
    try:
        return api_instance.get_event_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching event info using ext_id",
        )
