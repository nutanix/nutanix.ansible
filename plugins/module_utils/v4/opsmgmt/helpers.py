# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_report(module, api_instance, ext_id):
    """
    Fetch a single generated report instance by its external ID.

    Args:
        module (AnsibleModule): The Ansible module instance (used to fail
            gracefully on SDK errors).
        api_instance (ntnx_opsmgmt_py_client.ReportsApi): Reports API instance.
        ext_id (str): The external UUID of the report to fetch.

    Returns:
        The report data object returned by the SDK.
    """
    try:
        return api_instance.get_report_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report info using ext_id",
        )


def get_report_config(module, api_instance, ext_id):
    """
    Fetch a report configuration by its external ID. Primarily used to
    validate that a ``config_ext_id`` referenced in a report generation
    request exists before creating a report.

    Args:
        module (AnsibleModule): The Ansible module instance.
        api_instance (ntnx_opsmgmt_py_client.ReportConfigApi): Report config
            API instance.
        ext_id (str): The external UUID of the report configuration.

    Returns:
        The report configuration data object returned by the SDK.
    """
    try:
        return api_instance.get_report_config_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report configuration info using ext_id",
        )
