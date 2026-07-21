# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_report_config(module, api_instance, ext_id):
    """
    This method will return report configuration info using its ext_id.
    Args:
        module: Ansible module
        api_instance: ReportConfigApi instance from ntnx_opsmgmt_py_client sdk
        ext_id (str): report configuration external ID
    return:
        info (object): report configuration info
    """
    try:
        return api_instance.get_report_config_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report configuration info using ext_id",
        )
