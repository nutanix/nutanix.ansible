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
    import ntnx_iam_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    config = ntnx_iam_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    client = ntnx_iam_py_client.ApiClient(
        configuration=config, allow_version_negotiation=ALLOW_VERSION_NEGOTIATION
    )

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


def get_etag(data):
    """
    This method will fetch etag from a v4 api response.
    Args:
        data (dict): v4 api response
    """
    return ntnx_iam_py_client.ApiClient.get_etag(data)


def get_authorization_policy_api_instance(module):
    """
    This method will create authorization policies api instance
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): Authorization policy api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.AuthorizationPoliciesApi(api_client=api_client)


def get_directory_service_api_instance(module):
    """
    This method will return directory service api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): Directory service api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.DirectoryServicesApi(api_client=api_client)


def get_user_group_api_instance(module):
    """
    This method will return user group api instance.
    Args:
        module (AnsibleModule): Ansible module object
    Returns:
        api_instance (object): User group api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.UserGroupsApi(api_client=api_client)


def get_role_api_instance(module):
    """
    This method will return role api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): Role api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.RolesApi(api_client=api_client)


def get_permission_api_instance(module):
    """
    This method will return permission api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): Permission api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.OperationsApi(api_client=api_client)


def get_user_api_instance(module):
    """
    This method will return user api instance.
    Args:
        module (object): Ansible module object
    Returns:
        api_instance (object): User api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.UsersApi(api_client=api_client)


def get_identity_provider_api_instance(module):
    """
    This method will return SAMLIdentityProvidersApi instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): Identity provider api instance
    """
    api_client = get_api_client(module)
    return ntnx_iam_py_client.SAMLIdentityProvidersApi(api_client=api_client)
