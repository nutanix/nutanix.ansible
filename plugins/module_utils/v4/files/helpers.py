# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_unified_namespace(module, api_instance, ext_id):
    """
    Fetch a Nutanix Files Unified Namespace by external identifier.

    Args:
        module (AnsibleModule): The Ansible module used for error reporting.
        api_instance (ntnx_files_py_client.UnifiedNamespacesApi): API receiver
            used to issue the get-by-id call.
        ext_id (str): External identifier of the Unified Namespace.

    Returns:
        object: The Unified Namespace model returned by the SDK, or the module
        fails with a descriptive error when the API call raises.
    """
    try:
        return api_instance.get_unified_namespace_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching unified namespace info using ext_id",
        )
