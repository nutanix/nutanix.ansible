from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from base64 import b64encode

from ansible.module_utils.basic import missing_required_lib

FILES_SDK_IMP_ERROR = None
try:
    import ntnx_files_pc_py_client
except ImportError:
    FILES_SDK_IMP_ERROR = traceback.format_exc()


def get_files_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if FILES_SDK_IMP_ERROR:
        module.fail_json(
            missing_required_lib("ntnx_files_pc_py_client"), FILES_SDK_IMP_ERROR
        )

    config = ntnx_files_pc_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    client = ntnx_files_pc_py_client.ApiClient(configuration=config)

    cred = "{0}:{1}".format(config.username, config.password)
    try:
        encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
    except BaseException:
        encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
    auth_header = "Basic " + encoded_cred
    client.add_default_header(header_name="Authorization", header_value=auth_header)
    return client


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    """
    return ntnx_files_pc_py_client.ApiClient.get_etag(data)
