# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx proxy operations
    DOCUMENTATION = r"""
options:
  https_proxy:
    description:
      - The URL of the HTTPS proxy to use.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(http_proxy) -> C(all_proxy) module params, then C(HTTPS_PROXY) -> C(HTTP_PROXY) -> C(ALL_PROXY) env vars."
      - All module parameters (lowercase) are checked first, then environment variables (uppercase) as fallback.
    type: str
  http_proxy:
    description:
      - The URL of the HTTP proxy to use.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(http_proxy) -> C(all_proxy) module params, then C(HTTPS_PROXY) -> C(HTTP_PROXY) -> C(ALL_PROXY) env vars."
      - All module parameters (lowercase) are checked first, then environment variables (uppercase) as fallback.
    type: str
  all_proxy:
    description:
      - The URL of the proxy to use for all protocols.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(http_proxy) -> C(all_proxy) module params, then C(HTTPS_PROXY) -> C(HTTP_PROXY) -> C(ALL_PROXY) env vars."
      - All module parameters (lowercase) are checked first, then environment variables (uppercase) as fallback.
    type: str
  no_proxy:
    description:
      - Comma-separated list of hosts or domains to bypass the proxy.
      - "Precedence (highest to lowest): C(no_proxy) module param -> C(NO_PROXY) environment variable."
    type: str
  proxy_username:
    description:
      - The username for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): URL-embedded credentials -> C(proxy_username) module param -> C(PROXY_USERNAME) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
  proxy_password:
    description:
      - The password for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): URL-embedded credentials -> C(proxy_password) module param -> C(PROXY_PASSWORD) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
"""
