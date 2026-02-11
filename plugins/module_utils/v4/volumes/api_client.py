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

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def _get_proxy_url(module=None):
    """
    Get proxy URL from module parameters (preferred) or environment variables.

    Precedence (highest to lowest):
        https_proxy -> http_proxy -> all_proxy  (module params, lowercase)
        HTTPS_PROXY -> HTTP_PROXY -> ALL_PROXY  (environment variables, uppercase)
    """
    proxy_names = [
        "https_proxy",
        "http_proxy",
        "all_proxy",
    ]
    # Check module params first (lowercase)
    for name in proxy_names:
        if name in module.params:
            proxy_url = module.params.get(name)
            if proxy_url:
                return proxy_url
    # Fall back to environment variables (uppercase)
    for name in proxy_names:
        proxy_url = os.environ.get(name.upper())
        if proxy_url:
            return proxy_url
    return None


def _detect_no_proxy(host, module=None):
    """
    Detect if the 'no_proxy' environment variable is set and honor those locations.
    """
    env_no_proxy = module.params.get("no_proxy") or os.environ.get("NO_PROXY")
    if env_no_proxy:
        env_no_proxy = env_no_proxy.split(",")
        netloc = host or ""

        for no_proxy_host in env_no_proxy:
            if netloc.endswith(no_proxy_host) or netloc.split(":")[0].endswith(
                no_proxy_host
            ):
                # Our requested host matches something in no_proxy, so don't
                # use the proxy for this
                return False
    return True


def _apply_proxy_from_env(config, module=None):
    """
    Apply proxy configuration from environment variables.

    Supports credentials either embedded in URL or via separate environment variables:
    - Embedded: http://username:password@proxy:port
    - Separate: PROXY_USERNAME and PROXY_PASSWORD environment variables
    """
    if not _detect_no_proxy(config.host, module):
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

    # Get credentials from URL first, then fall back to separate environment variables
    if parsed.username:
        config.proxy_username = unquote(parsed.username)
    else:
        config.proxy_username = module.params.get("proxy_username") or os.environ.get(
            "PROXY_USERNAME"
        )

    if parsed.password:
        config.proxy_password = unquote(parsed.password)
    else:
        config.proxy_password = module.params.get("proxy_password") or os.environ.get(
            "PROXY_PASSWORD"
        )


def get_api_client(module):
    """
    This method will return client to be used in api connection using
    given connection details.
    """
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    config = ntnx_volumes_py_client.Configuration()
    config.host = module.params.get("nutanix_host")
    config.port = module.params.get("nutanix_port")
    config.username = module.params.get("nutanix_username")
    config.password = module.params.get("nutanix_password")
    config.verify_ssl = module.params.get("validate_certs")
    _apply_proxy_from_env(config, module)
    client = ntnx_volumes_py_client.ApiClient(
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
    return ntnx_volumes_py_client.ApiClient.get_etag(data)


def get_vg_api_instance(module):
    """
    This method will return VolumeGroupApi instance.
    """
    client = get_api_client(module)
    return ntnx_volumes_py_client.VolumeGroupsApi(api_client=client)


def get_iscsi_client_api_instance(module):
    """
    This method will return IscsiClientApi instance.
    """
    client = get_api_client(module)
    return ntnx_volumes_py_client.IscsiClientsApi(api_client=client)
