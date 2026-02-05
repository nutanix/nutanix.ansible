# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

from ...constants import ALLOW_VERSION_NEGOTIATION
from ..api_logger import setup_api_logging

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    config = ntnx_vmm_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    api_key = module.params.get("nutanix_api_key")
    nutanix_username = module.params.get("nutanix_username")
    nutanix_password = module.params.get("nutanix_password")
    if (not nutanix_username or not nutanix_password) and not (api_key):
        module.fail_json(msg="Either nutanix_username and nutanix_password or nutanix_api_key is required")
    if api_key:
        config.set_api_key(api_key)
    else:
        config.username = nutanix_username
        config.password = nutanix_password
    config.verify_ssl = module.params.get("validate_certs")
    client = ntnx_vmm_py_client.ApiClient(
        configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
    )

    if not api_key:
        cred = "{0}:{1}".format(config.username, config.password)
        try:
            encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
        except BaseException:
            encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
        auth_header = "Basic " + encoded_cred
        client.add_default_header(header_name="Authorization", header_value=auth_header)

    # Setup API logging if debug is enabled
    setup_api_logging(module, client)

    return client


def get_vm_api_instance(module):
    """
    This method will return VMM API instance
    Args:
        api_instance (obj): v4 VMM api instance
    """
    api_client = get_api_client(module)
    return ntnx_vmm_py_client.VmApi(api_client=api_client)


def get_image_api_instance(module):
    """
    This method will return Image API instance
    Args:
        api_instance (obj): v4 Image api instance
    """
    api_client = get_api_client(module)
    return ntnx_vmm_py_client.ImagesApi(api_client=api_client)


def get_image_placement_policy_api_instance(module):
    """
    This method will return Image Placement policy API instance
    Args:
        api_instance (obj): v4 Image placement policy api instance
    """
    api_client = get_api_client(module)
    return ntnx_vmm_py_client.ImagePlacementPoliciesApi(api_client=api_client)


def get_templates_api_instance(module):
    """
    This method will return Templates API instance
    Args:
        api_instance (obj): v4 Templates api instance
    """
    api_client = get_api_client(module)
    return ntnx_vmm_py_client.TemplatesApi(api_client=api_client)


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    """
    return ntnx_vmm_py_client.ApiClient.get_etag(data)


def get_ova_api_instance(module):
    """
    This method will return OVA API instance
    Args:
        api_instance (obj): v4 OVA api instance
    """
    api_client = get_api_client(module)
    return ntnx_vmm_py_client.OvasApi(api_client=api_client)
