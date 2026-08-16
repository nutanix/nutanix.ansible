# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

from ..api_logger import setup_api_logging
from ..utils import _apply_proxy_from_env

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def _new_api_client(config):
    """
    Instantiate ``ApiClient`` from the storage SDK.

    The storage SDK's ``ApiClient`` currently accepts only ``configuration``;
    other Nutanix v4 SDKs accept an ``allow_version_negotiation`` flag as well.
    Try the extended signature first for forward compatibility, then fall back
    to the plain one so this helper keeps working across SDK revisions.
    """
    try:
        return ntnx_storage_py_client.ApiClient(
            configuration=config, allow_version_negotiation=True
        )
    except TypeError:
        return ntnx_storage_py_client.ApiClient(configuration=config)


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details for the storage namespace v4 SDK.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"), exception=SDK_IMP_ERROR
        )

    config = ntnx_storage_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    api_key = module.params.get("nutanix_api_key")
    nutanix_username = module.params.get("nutanix_username")
    nutanix_password = module.params.get("nutanix_password")
    if (not nutanix_username or not nutanix_password) and not api_key:
        module.fail_json(
            msg="Either nutanix_username and nutanix_password or nutanix_api_key is required"
        )
    if api_key:
        config.set_api_key(api_key)
    else:
        config.username = nutanix_username
        config.password = nutanix_password
    config.verify_ssl = module.params.get("validate_certs")
    config.read_timeout = module.params.get("read_timeout")
    _apply_proxy_from_env(config, module)
    client = _new_api_client(config)

    if not api_key:
        cred = "{0}:{1}".format(config.username, config.password)
        try:
            encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
        except BaseException:
            encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
        auth_header = "Basic " + encoded_cred
        client.add_default_header(header_name="Authorization", header_value=auth_header)

    setup_api_logging(module, client)

    return client


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    """
    return ntnx_storage_py_client.ApiClient.get_etag(data)


def get_vg_api_instance(module):
    """
    This method will return VolumeGroupApi instance backed by the storage v4 SDK.
    """
    client = get_api_client(module)
    return ntnx_storage_py_client.VolumeGroupApi(api_client=client)
