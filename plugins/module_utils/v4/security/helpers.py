# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_stig_controls_details(module, api_instance, **kwargs):
    """
    This method will return STIG controls details on each cluster.
    Args:
        module: Ansible module
        api_instance: STIGsApi instance from ntnx_security_py_client sdk
    return:
        stig_control_info (object): STIG control info
    """
    try:
        return api_instance.list_stigs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching STIG control details",
        )
