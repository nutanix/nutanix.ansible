# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_audit(module, api_instance, ext_id):
    """
    This method will return audit info using its ext_id.

    Args:
        module (object): Ansible module object
        api_instance (object): AuditsApi instance from ntnx_monitoring_py_client
        ext_id (str): Audit external ID
    return:
        info (object): audit info
    """
    try:
        return api_instance.get_audit_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching audit info using ext_id: {0}".format(
                ext_id
            ),
        )
