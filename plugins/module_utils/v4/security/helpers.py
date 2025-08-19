# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_kms_by_ext_id(module, api_instance, ext_id):
    """
    This method will return KMS info using external ID.
    Args:
        module: Ansible module
        api_instance: KMSApi instance from ntnx_security_py_client sdk
        ext_id: External ID of the KMS
    """
    try:
        return api_instance.get_key_management_server_by_id(ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching KMS info using external ID",
        )

def list_kms(module, api_instance):
    """
    This method will return a list of all KMS instances.
    Args:
        module: Ansible module
        api_instance: KMSApi instance from ntnx_security_py_client sdk
    """
    try:
        return api_instance.list_key_management_servers()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching KMS list",
        )