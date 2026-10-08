# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import os

import pytest
from ansible_collections.nutanix.ncp.plugins.module_utils.utils import (
    get_custom_headers,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.v4.api_logger import APILogger
from ansible_collections.nutanix.ncp.plugins.module_utils.v4.utils import (
    _apply_custom_headers,
)


@pytest.fixture(autouse=True)
def clean_header_env(monkeypatch):
    """Remove any NUTANIX_HEADER_ variables from the test environment."""
    for key in list(os.environ):
        if key.startswith("NUTANIX_HEADER_"):
            monkeypatch.delenv(key)


class FakeClient:
    def __init__(self):
        self.headers = {}

    def add_default_header(self, header_name, header_value):
        self.headers[header_name] = header_value


class FakeModule:
    def __init__(self, params):
        self.params = params
        self.no_log_values = set()


def test_env_var_converted_to_header(monkeypatch):
    monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "env-id")
    assert get_custom_headers({}) == {"Cf-Access-Client-Id": "env-id"}


def test_other_env_vars_ignored(monkeypatch):
    monkeypatch.setenv("NUTANIX_HOST", "pc.example.com")
    assert get_custom_headers({}) == {}


def test_empty_header_name_skipped(monkeypatch):
    monkeypatch.setenv("NUTANIX_HEADER_", "value")
    assert get_custom_headers({}) == {}


def test_config_overrides_env_case_insensitively(monkeypatch):
    monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "env-id")
    monkeypatch.setenv("NUTANIX_HEADER_X_OTHER", "env-other")
    headers = get_custom_headers(
        {"custom_headers": {"CF-Access-Client-Id": "config-id"}}
    )
    assert headers == {"CF-Access-Client-Id": "config-id", "X-Other": "env-other"}


class _VaultLike(object):
    """Stands in for a vault-encrypted inventory value: not a str, but str() works."""

    def __str__(self):
        return "vault-secret"


def test_non_str_config_value_converted_to_text():
    # The SDK treats any non-primitive header value as a model and fails on it.
    headers = get_custom_headers({"custom_headers": {"X-Secret": _VaultLike()}})
    assert headers == {"X-Secret": "vault-secret"}
    assert isinstance(headers["X-Secret"], str)


def test_apply_custom_headers_sets_headers_and_no_log(monkeypatch):
    monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "env-secret")
    module = FakeModule({"custom_headers": {"Cf-Access-Client-Id": "config-id"}})
    client = FakeClient()

    _apply_custom_headers(client, module)

    assert client.headers == {
        "Cf-Access-Client-Secret": "env-secret",
        "Cf-Access-Client-Id": "config-id",
    }
    # Values from the environment are masked in module output, like the option.
    assert {"env-secret", "config-id"} <= module.no_log_values


def test_debug_log_redacts_custom_headers():
    module = FakeModule(
        {"custom_headers": {"X-Client-Key": "k"}, "nutanix_debug": False}
    )
    logger = APILogger(module)
    sanitized = logger._sanitize_headers(
        {"X-Client-Key": "k", "Accept": "application/json"}
    )
    assert sanitized == {"X-Client-Key": "***REDACTED***", "Accept": "application/json"}


def test_every_v4_api_client_applies_custom_headers():
    """Each v4 SDK client builder must apply the custom headers."""
    here = os.path.dirname(os.path.abspath(__file__))
    v4_dir = os.path.join(here, "..", "..", "..", "..", "plugins", "module_utils", "v4")
    paths = glob.glob(os.path.join(v4_dir, "*", "api_client.py")) + glob.glob(
        os.path.join(v4_dir, "*", "pc_api_client.py")
    )
    assert paths, "no v4 api client modules found"
    missing = []
    for path in paths:
        with open(path) as f:
            if "_apply_custom_headers(client, module)" not in f.read():
                missing.append(path)
    assert not missing, "v4 clients that do not apply custom headers: %s" % missing
