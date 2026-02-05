# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import traceback
from base64 import b64encode

try:
    # Python 3
    from urllib.parse import unquote, urlparse
except ImportError:
    # Python 2.7
    from urlparse import urlparse
    from urllib import unquote

from ansible.module_utils.basic import missing_required_lib

from ...constants import ALLOW_VERSION_NEGOTIATION
from ..api_logger import setup_api_logging

PRISM_SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client
except ImportError:
    PRISM_SDK_IMP_ERROR = traceback.format_exc()


def _get_proxy_url(module):
    """
    Get proxy URL from module params first, then fall back to environment variables.

    Checks module params first, then common proxy environment variable names.
    """
    proxy_vars = [
        "https_proxy",
        "HTTPS_PROXY",
        "http_proxy",
        "HTTP_PROXY",
        "all_proxy",
        "ALL_PROXY",
    ]

    # First check module params
    for var in proxy_vars:
        proxy_url = module.params.get(var)
        if proxy_url:
            return proxy_url

    # Fall back to environment variables
    for var in proxy_vars:
        proxy_url = os.environ.get(var)
        if proxy_url:
            return proxy_url

    return None


def _detect_no_proxy(module, host):
    """
    Detect if proxy should be bypassed for the given host.

    Checks module params first, then no_proxy environment variable.
    """
    no_proxy_vars = ["no_proxy", "NO_PROXY"]

    # First check module params
    no_proxy = None
    for var in no_proxy_vars:
        no_proxy = module.params.get(var)
        if no_proxy:
            break

    # Fall back to environment variables
    if not no_proxy:
        for var in no_proxy_vars:
            no_proxy = os.environ.get(var)
            if no_proxy:
                break

    if no_proxy:
        no_proxy_list = no_proxy.split(",")
        netloc = host or ""

        for no_proxy_host in no_proxy_list:
            no_proxy_host = no_proxy_host.strip()
            if netloc.endswith(no_proxy_host) or netloc.split(":")[0].endswith(
                no_proxy_host
            ):
                # Our requested host matches something in no_proxy, so don't
                # use the proxy for this
                return False
    return True


def _apply_proxy_from_env(module, config):
    """
    Apply proxy configuration from module params or environment variables.
    """
    if not _detect_no_proxy(module, config.host):
        return

    proxy_url = _get_proxy_url(module)
    if not proxy_url:
        return

    parsed = urlparse(proxy_url)
    if not parsed.hostname or parsed.scheme == "":
        return

    config.proxy_scheme = parsed.scheme
    config.proxy_host = parsed.hostname
    config.proxy_port = parsed.port or 443
    config.proxy_username = unquote(parsed.username) if parsed.username else None
    config.proxy_password = unquote(parsed.password) if parsed.password else None


def get_pc_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if PRISM_SDK_IMP_ERROR:
        module.fail_json(
            missing_required_lib("ntnx_prism_py_client"), exception=PRISM_SDK_IMP_ERROR
        )

    config = ntnx_prism_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    _apply_proxy_from_env(module, config)
    client = ntnx_prism_py_client.ApiClient(
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
    return ntnx_prism_py_client.ApiClient.get_etag(data)


def get_domain_manager_api_instance(module):
    """
    This method will return domain manager api instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): domain manager api instance
    """
    api_client = get_pc_api_client(module)
    return ntnx_prism_py_client.DomainManagerApi(api_client=api_client)


def get_domain_manager_backup_api_instance(module):
    """
    This method will return domain manager backup api instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): domain manager backup api instance
    """
    api_client = get_pc_api_client(module)
    return ntnx_prism_py_client.DomainManagerBackupsApi(api_client=api_client)


def get_tasks_api_instance(module):
    """
    This method will return tasks api instance.
    Args:
        module (object): Ansible module object
    return:
        api_instance (object): tasks api instance
    """
    api_client = get_pc_api_client(module)
    return ntnx_prism_py_client.TasksApi(api_client=api_client)
