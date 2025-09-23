# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_licensing_key(module, api_instance, license_key_ext_id):
    """
    This method will return license key info using external ID.
    Args:
        module: Ansible module
        api_instance: LicensingKeysApi instance from ntnx_licensing_py_client sdk
        license_key_ext_id (str): license key external ID
    Returns:
        license_key_info (object): license key info
    """
    try:
        return api_instance.get_license_key_by_id(extId=license_key_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching license key info using ext_id",
        )
