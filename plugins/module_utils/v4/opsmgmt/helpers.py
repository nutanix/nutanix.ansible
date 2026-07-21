# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_report(module, api_instance, ext_id):
    """
    Fetch a report instance by its external ID.

    Args:
        module (AnsibleModule): Ansible module used to fail fast on API errors.
        api_instance (ntnx_opsmgmt_py_client.ReportsApi): ReportsApi instance.
        ext_id (str): External ID (UUID) of the report instance.

    Returns:
        object: The report SDK object (``resp.data``) when the call succeeds.
    """
    try:
        return api_instance.get_report_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report info using ext_id",
        )
