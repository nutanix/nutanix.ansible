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
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  HTTPS_PROXY:
    description:
      - The URL of the HTTPS proxy to use.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  http_proxy:
    description:
      - The URL of the HTTP proxy to use.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  HTTP_PROXY:
    description:
      - The URL of the HTTP proxy to use.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  all_proxy:
    description:
      - The URL of the proxy to use for all protocols.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  ALL_PROXY:
    description:
      - The URL of the proxy to use for all protocols.
      - "Proxy URL precedence (highest to lowest): C(https_proxy) -> C(HTTPS_PROXY) -> C(http_proxy) -> C(HTTP_PROXY) -> C(all_proxy) -> C(ALL_PROXY)."
      - Module parameters take precedence over environment variables.
    type: str
  no_proxy:
    description:
      - Comma-separated list of hosts or domains to bypass the proxy.
      - "Precedence (highest to lowest): C(no_proxy) -> C(NO_PROXY) module param -> C(no_proxy) -> C(NO_PROXY) environment variable."
    type: str
  NO_PROXY:
    description:
      - Comma-separated list of hosts or domains to bypass the proxy.
      - "Precedence (highest to lowest): C(no_proxy) -> C(NO_PROXY) module param -> C(no_proxy) -> C(NO_PROXY) environment variable."
    type: str
  proxy_username:
    description:
      - The username for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): C(proxy_username) -> C(PROXY_USERNAME) module param -> C(PROXY_USERNAME) -> C(proxy_username) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
  PROXY_USERNAME:
    description:
      - The username for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): C(proxy_username) -> C(PROXY_USERNAME) module param -> C(PROXY_USERNAME) -> C(proxy_username) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
  proxy_password:
    description:
      - The password for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): C(proxy_password) -> C(PROXY_PASSWORD) module param -> C(PROXY_PASSWORD) -> C(proxy_password) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
  PROXY_PASSWORD:
    description:
      - The password for proxy authentication (if not embedded in proxy URL).
      - "Precedence (highest to lowest): C(proxy_password) -> C(PROXY_PASSWORD) module param -> C(PROXY_PASSWORD) -> C(proxy_password) environment variable."
      - If credentials are embedded in the proxy URL (e.g., C(http://user:pass@proxy:port)), they take precedence.
    type: str
"""
