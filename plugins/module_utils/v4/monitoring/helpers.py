# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_uda_policy(module, api_instance, ext_id):
    """
    Fetch a User-Defined Alert policy by its external ID.

    Args:
        module (AnsibleModule): Ansible module object.
        api_instance (UserDefinedPoliciesApi): Monitoring SDK API instance.
        ext_id (str): User-Defined Alert policy external ID.
    Returns:
        object: SDK response wrapper for the fetched policy.
    """
    try:
        return api_instance.get_uda_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching User-Defined Alert policy info using ext_id",
        )
