# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_virus_scan_policy(module, api_instance, file_server_ext_id, ext_id):
    """
    Fetch a virus scan policy by its external ID under the given file server.

    Args:
        module (AnsibleModule): Ansible module used for error handling.
        api_instance: VirusScanPoliciesApi instance.
        file_server_ext_id (str): External ID of the parent file server.
        ext_id (str): External ID of the virus scan policy.

    Returns:
        object: The virus scan policy model returned by the SDK.
    """
    try:
        return api_instance.get_virus_scan_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virus scan policy info using ext_id",
        )


def list_virus_scan_policies(module, api_instance, file_server_ext_id, **kwargs):
    """
    List virus scan policies for the given file server, honoring optional
    OData params (filter/limit/page/orderby/select) passed via kwargs.

    Args:
        module (AnsibleModule): Ansible module used for error handling.
        api_instance: VirusScanPoliciesApi instance.
        file_server_ext_id (str): External ID of the parent file server.
        **kwargs: Optional OData parameters (``_page``, ``_limit``,
            ``_filter``, ``_orderby``, ``_select``).

    Returns:
        object: The raw list response returned by the SDK.
    """
    try:
        return api_instance.list_virus_scan_policies(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virus scan policies info",
        )
