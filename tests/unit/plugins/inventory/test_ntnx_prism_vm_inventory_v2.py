# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for ntnx_prism_vm_inventory_v2 inventory plugin.

Includes:
  - Pure unit tests for get_custom_headers() env-var parsing and precedence.
  - Unit tests verifying custom headers are applied to the API client.
  - A live integration test (skipped unless NUTANIX_HOST + NUTANIX_API_KEY are set)
    that retrieves VMs from Prism Central using API key auth and NUTANIX_HEADER_*
    custom headers (e.g. Cloudflare Access tokens).

Run unit tests only:
    pytest tests/unit/plugins/inventory/test_ntnx_prism_vm_inventory_v2.py -v -m "not live"

Run all tests (requires sourced .env with NUTANIX_HOST, NUTANIX_API_KEY,
NUTANIX_HEADER_CF_ACCESS_CLIENT_ID, NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET):
    source inventory/landscape/.env
    pytest tests/unit/plugins/inventory/test_ntnx_prism_vm_inventory_v2.py -v -s
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

import pytest

# ---------------------------------------------------------------------------
# Ensure the ansible_collections namespace is importable.
# The installed collection lives at:
#   ~/.ansible/collections/ansible_collections/nutanix/ncp/
# Adding ~/.ansible/collections to sys.path makes
#   ansible_collections.nutanix.ncp  resolvable.
# ---------------------------------------------------------------------------
_COLLECTIONS_PATH = os.path.expanduser("~/.ansible/collections")
if _COLLECTIONS_PATH not in sys.path:
    sys.path.insert(0, _COLLECTIONS_PATH)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 1. Unit tests: get_custom_headers()
# ---------------------------------------------------------------------------


class TestGetCustomHeaders:
    """Tests for the get_custom_headers() utility that converts NUTANIX_HEADER_*
    environment variables into HTTP header dicts."""

    def _fn(self):
        from ansible_collections.nutanix.ncp.plugins.module_utils.utils import (
            get_custom_headers,
        )

        return get_custom_headers

    def test_single_env_var_converted_to_header(self, monkeypatch):
        """NUTANIX_HEADER_X_CUSTOM_TOKEN -> X-Custom-Token"""
        monkeypatch.setenv("NUTANIX_HEADER_X_CUSTOM_TOKEN", "abc123")
        headers = self._fn()({})
        assert headers.get("X-Custom-Token") == "abc123"

    def test_cf_access_client_id_conversion(self, monkeypatch):
        """NUTANIX_HEADER_CF_ACCESS_CLIENT_ID -> Cf-Access-Client-Id"""
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "test-client-id")
        headers = self._fn()({})
        assert headers.get("Cf-Access-Client-Id") == "test-client-id"

    def test_cf_access_client_secret_conversion(self, monkeypatch):
        """NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET -> Cf-Access-Client-Secret"""
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "test-secret")
        headers = self._fn()({})
        assert headers.get("Cf-Access-Client-Secret") == "test-secret"

    def test_multiple_env_vars_all_collected(self, monkeypatch):
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "id-val")
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "secret-val")
        headers = self._fn()({})
        assert headers.get("Cf-Access-Client-Id") == "id-val"
        assert headers.get("Cf-Access-Client-Secret") == "secret-val"

    def test_no_env_vars_returns_empty(self, monkeypatch):
        for key in list(os.environ.keys()):
            if key.startswith("NUTANIX_HEADER_"):
                monkeypatch.delenv(key)
        headers = self._fn()({})
        assert headers == {}

    def test_config_headers_take_precedence_over_env(self, monkeypatch):
        """Explicitly set custom_headers in config override env vars."""
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "env-value")
        headers = self._fn()(
            {"custom_headers": {"Cf-Access-Client-Id": "config-value"}}
        )
        assert headers["Cf-Access-Client-Id"] == "config-value"

    def test_env_and_config_headers_merged(self, monkeypatch):
        """Env-var headers and config headers are merged; config wins on conflict."""
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "env-id")
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "env-secret")
        headers = self._fn()({"custom_headers": {"Cf-Access-Client-Id": "config-id"}})
        assert headers["Cf-Access-Client-Id"] == "config-id"
        assert headers["Cf-Access-Client-Secret"] == "env-secret"

    def test_non_nutanix_header_env_vars_ignored(self, monkeypatch):
        monkeypatch.setenv("SOME_OTHER_VAR", "ignored")
        monkeypatch.setenv("NUTANIX_HOST", "host-ignored")
        for key in list(os.environ.keys()):
            if key.startswith("NUTANIX_HEADER_"):
                monkeypatch.delenv(key)
        headers = self._fn()({})
        assert headers == {}


# ---------------------------------------------------------------------------
# 2. Unit tests: custom headers applied to API client
# ---------------------------------------------------------------------------


class TestCustomHeadersAppliedToApiClient:
    """Verify that _apply_custom_headers() adds all headers returned by
    get_custom_headers() to the SDK ApiClient via add_default_header()."""

    def test_headers_added_to_client(self, monkeypatch):
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "test-id")
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "test-secret")

        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_module = MagicMock()
        mock_module.params = {"custom_headers": None}

        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.utils import (
            _apply_custom_headers,
        )

        _apply_custom_headers(mock_client, mock_module)

        added = {
            call.kwargs.get("header_name")
            or call.args[0]: call.kwargs.get("header_value")
            or call.args[1]
            for call in mock_client.add_default_header.call_args_list
        }
        assert added.get("Cf-Access-Client-Id") == "test-id"
        assert added.get("Cf-Access-Client-Secret") == "test-secret"

    def test_no_headers_added_when_env_empty(self, monkeypatch):
        for key in list(os.environ.keys()):
            if key.startswith("NUTANIX_HEADER_"):
                monkeypatch.delenv(key)

        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_module = MagicMock()
        mock_module.params = {"custom_headers": None}

        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.utils import (
            _apply_custom_headers,
        )

        _apply_custom_headers(mock_client, mock_module)
        mock_client.add_default_header.assert_not_called()


# ---------------------------------------------------------------------------
# 3. Parametrised unit tests: every v4 API client calls _apply_custom_headers
# ---------------------------------------------------------------------------

_V4_API_CLIENTS = [
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.vmm.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.clusters_mgmt.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.network.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.iam.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.flow.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.data_protection.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.data_policies.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.volumes.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.objects.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.security.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.lcm.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.licensing.api_client",
    "ansible_collections.nutanix.ncp.plugins.module_utils.v4.prism.pc_api_client",
]

_SDK_MODULES = {
    "vmm": "ntnx_vmm_py_client",
    "clusters_mgmt": "ntnx_clustermgmt_py_client",
    "network": "ntnx_networking_py_client",
    "iam": "ntnx_iam_py_client",
    "flow": "ntnx_microseg_py_client",
    "data_protection": "ntnx_dataprotection_py_client",
    "data_policies": "ntnx_datapolicies_py_client",
    "volumes": "ntnx_volumes_py_client",
    "objects": "ntnx_objects_py_client",
    "security": "ntnx_security_py_client",
    "lcm": "ntnx_lifecycle_py_client",
    "licensing": "ntnx_licensing_py_client",
    "prism": "ntnx_prism_py_client",
}

# Some clients use a name other than get_api_client
_GET_API_CLIENT_FN = {
    "prism": "get_pc_api_client",
}


def _client_id(module_path):
    """Pytest ID: use the API area name (e.g. 'vmm', 'iam')."""
    return module_path.split(".")[-2]


@pytest.mark.parametrize("client_module_path", _V4_API_CLIENTS, ids=_client_id)
class TestAllV4ClientsApplyCustomHeaders:
    """For every v4 API client, verify that get_api_client() calls
    _apply_custom_headers(), which adds NUTANIX_HEADER_* env vars as HTTP
    headers on the SDK ApiClient instance.

    The underlying SDK packages are mocked so no network access is needed.
    """

    def _make_mock_module(self):
        from unittest.mock import MagicMock

        module = MagicMock()
        module.params = {
            "nutanix_host": "10.0.0.1",
            "nutanix_port": "9440",
            "nutanix_username": None,
            "nutanix_password": None,
            "nutanix_api_key": "test-api-key",
            "validate_certs": False,
            "nutanix_debug": False,
            "nutanix_log_file": None,
            "custom_headers": None,
            "load_params_without_defaults": False,
            "https_proxy": None,
            "http_proxy": None,
            "all_proxy": None,
            "no_proxy": None,
        }
        module.fail_json.side_effect = Exception("fail_json called")
        return module

    def test_custom_headers_applied(self, client_module_path, monkeypatch):
        """get_api_client() must add NUTANIX_HEADER_* env vars to the client."""
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID", "test-cf-id")
        monkeypatch.setenv("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET", "test-cf-secret")

        import importlib
        from unittest.mock import MagicMock, patch

        # Derive which SDK package this client imports
        api_area = client_module_path.split(".")[-2]
        sdk_name = _SDK_MODULES[api_area]

        # Build a minimal mock SDK that satisfies get_api_client()
        mock_sdk = MagicMock()
        mock_config = MagicMock()
        mock_client = MagicMock()
        mock_sdk.Configuration.return_value = mock_config
        mock_sdk.ApiClient.return_value = mock_client

        with patch.dict("sys.modules", {sdk_name: mock_sdk}):
            client_mod = importlib.import_module(client_module_path)
            importlib.reload(client_mod)

            fn_name = _GET_API_CLIENT_FN.get(api_area, "get_api_client")
            module = self._make_mock_module()
            getattr(client_mod, fn_name)(module)

        added = {
            call.kwargs.get("header_name")
            or call.args[0]: (call.kwargs.get("header_value") or call.args[1])
            for call in mock_client.add_default_header.call_args_list
        }

        assert (
            "Cf-Access-Client-Id" in added
        ), f"{client_module_path}: Cf-Access-Client-Id missing from default headers"
        assert added["Cf-Access-Client-Id"] == "test-cf-id"
        assert (
            "Cf-Access-Client-Secret" in added
        ), f"{client_module_path}: Cf-Access-Client-Secret missing from default headers"
        assert added["Cf-Access-Client-Secret"] == "test-cf-secret"

    def test_no_custom_headers_when_env_empty(self, client_module_path, monkeypatch):
        """When no NUTANIX_HEADER_* env vars are set, no custom headers are added."""
        for key in list(os.environ.keys()):
            if key.startswith("NUTANIX_HEADER_"):
                monkeypatch.delenv(key)

        import importlib
        from unittest.mock import MagicMock, patch

        api_area = client_module_path.split(".")[-2]
        sdk_name = _SDK_MODULES[api_area]

        mock_sdk = MagicMock()
        mock_config = MagicMock()
        mock_client = MagicMock()
        mock_sdk.Configuration.return_value = mock_config
        mock_sdk.ApiClient.return_value = mock_client

        with patch.dict("sys.modules", {sdk_name: mock_sdk}):
            client_mod = importlib.import_module(client_module_path)
            importlib.reload(client_mod)

            fn_name = _GET_API_CLIENT_FN.get(api_area, "get_api_client")
            module = self._make_mock_module()
            getattr(client_mod, fn_name)(module)

        added_names = [
            call.kwargs.get("header_name") or call.args[0]
            for call in mock_client.add_default_header.call_args_list
        ]
        custom = [h for h in added_names if h.startswith("Cf-")]
        assert (
            custom == []
        ), f"{client_module_path}: unexpected custom headers added: {custom}"


# ---------------------------------------------------------------------------
# 4. Unit tests: parse() strips Ansible tagged string types from api_key
# ---------------------------------------------------------------------------


class _AnsibleTaggedStr(str):
    """Minimal stand-in for ansible.utils.unsafe_proxy.AnsibleUnsafeText /
    ansible.parsing.yaml.objects.AnsibleTaggedStr.

    Ansible's get_option() returns str *subclasses*, not plain str.  The VMM
    SDK's Configuration.set_api_key() uses ``type(key) is str`` (strict check),
    so a subclass value is treated as None and authentication silently breaks.
    """


class TestAnsibleTaggedStrApiKey:
    """Prove that parse() correctly handles _AnsibleTaggedStr api_key values.

    This test class captures the root cause of ansible-inventory --graph
    failing even when NUTANIX_API_KEY is set: Ansible's config layer wraps
    string option values in a str subclass (_AnsibleTaggedStr / AnsibleUnsafeText),
    and the Nutanix VMM SDK's Configuration.set_api_key() uses a strict
    ``type(key) is str`` check that rejects subclasses, silently setting the
    key to None.  The fix is to convert the api_key to plain str in parse().
    """

    def test_sdk_set_api_key_rejects_str_subclass(self):
        """Demonstrate the SDK bug: type(key) is str fails for str subclasses."""
        import ntnx_vmm_py_client

        config = ntnx_vmm_py_client.Configuration()
        tagged = _AnsibleTaggedStr("my-secret-api-key")
        config.set_api_key(tagged)

        # The SDK silently sets None because type(tagged) is not str
        assert (
            config.api_key.get("X-ntnx-api-key") is None
        ), "Expected SDK to reject str subclass (proving the known SDK limitation)"

    def test_sdk_set_api_key_accepts_plain_str(self):
        """Plain str always works with set_api_key."""
        import ntnx_vmm_py_client

        config = ntnx_vmm_py_client.Configuration()
        config.set_api_key("my-secret-api-key")

        assert config.api_key.get("X-ntnx-api-key") == "my-secret-api-key"

    def test_parse_converts_tagged_api_key_to_plain_str(self, monkeypatch):
        """parse() must call str() on the api_key so that the VMM SDK's strict
        type check accepts it.  This is the regression test for the root cause
        of ansible-inventory --graph failing silently.
        """
        from unittest.mock import patch as mock_patch

        from ansible.inventory.data import InventoryData
        from ansible.parsing.dataloader import DataLoader
        from ansible_collections.nutanix.ncp.plugins.inventory.ntnx_prism_vm_inventory_v2 import (
            InventoryModule,
        )

        # Use a str subclass (simulating Ansible's _AnsibleTaggedStr)
        tagged_api_key = _AnsibleTaggedStr("test-api-key-12345")
        assert type(tagged_api_key) is not str, "Pre-condition: must be a str subclass"

        captured_module = {}

        def fake_get_vm_api_instance(module):
            captured_module["module"] = module
            raise Exception("stop-early")

        with mock_patch(
            "ansible_collections.nutanix.ncp.plugins.inventory.ntnx_prism_vm_inventory_v2.get_vm_api_instance",
            side_effect=fake_get_vm_api_instance,
        ):
            options = {
                "nutanix_host": "10.0.0.1",
                "nutanix_port": "9440",
                "nutanix_username": None,
                "nutanix_password": None,
                "nutanix_api_key": tagged_api_key,
                "custom_headers": None,
                "validate_certs": False,
                "fetch_all_vms": False,
                "page": 0,
                "limit": 10,
                "filter": None,
                "custom_ansible_host": None,
                "nutanix_debug": False,
                "nutanix_log_file": None,
                "filters": [],
                "strict": False,
                "compose": {},
                "groups": {},
                "keyed_groups": [],
            }
            plugin = InventoryModule()
            with mock_patch.object(InventoryModule, "_read_config_data"):
                plugin._options = options
                try:
                    plugin.parse(
                        InventoryData(), DataLoader(), "nutanix.yaml", cache=False
                    )
                except Exception:
                    pass  # expected: we raised "stop-early"

        assert (
            "module" in captured_module
        ), "Mock_Module was not passed to get_vm_api_instance"
        module = captured_module["module"]
        stored_key = module.params.get("nutanix_api_key")
        assert type(stored_key) is str, (
            f"Expected plain str in Mock_Module.params['nutanix_api_key'], "
            f"got {type(stored_key).__name__!r}. "
            "parse() must convert get_option() results to plain str before "
            "passing to Mock_Module to avoid VMM SDK's strict type check failing."
        )
        assert stored_key == "test-api-key-12345"


# ---------------------------------------------------------------------------
# 5. Live integration test: list VMs via real Prism Central API
# ---------------------------------------------------------------------------

_LIVE_SKIP_REASON = (
    "Live test requires NUTANIX_HOST and NUTANIX_API_KEY environment variables. "
    "Source inventory/landscape/.env before running."
)


@pytest.mark.live
@pytest.mark.skipif(
    not os.environ.get("NUTANIX_HOST") or not os.environ.get("NUTANIX_API_KEY"),
    reason=_LIVE_SKIP_REASON,
)
class TestLiveListVms:
    """Integration test: exercises the full path from Mock_Module -> API client
    -> list_vms() against a real Prism Central instance.

    Validates:
    - API key authentication works.
    - NUTANIX_HEADER_CF_ACCESS_CLIENT_ID / _SECRET are sent as Cloudflare
      Access headers and the request is not rejected.
    - At least one page of VMs (or an empty list) is returned without error.
    """

    def _build_module(self):
        """Construct a Mock_Module using env vars from the sourced .env file."""
        from ansible_collections.nutanix.ncp.plugins.inventory.ntnx_prism_vm_inventory_v2 import (
            Mock_Module,
        )

        host = os.environ.get("NUTANIX_HOST") or os.environ.get("NUTANIX_HOSTNAME")
        port = os.environ.get("NUTANIX_PORT", "9440")
        api_key = os.environ.get("NUTANIX_API_KEY")

        return Mock_Module(
            hostname=host,
            port=port,
            username=None,
            password=None,
            validate_certs=False,
            nutanix_api_key=api_key,
            custom_headers=None,  # headers come from NUTANIX_HEADER_* env vars
        )

    def test_list_vms_returns_response(self):
        """list_vms() succeeds and returns a valid SDK response object."""
        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.vmm.api_client import (
            get_vm_api_instance,
        )

        module = self._build_module()
        vmm = get_vm_api_instance(module)

        resp = vmm.list_vms(_page=0, _limit=10)

        assert resp is not None, "Expected a response object from list_vms()"
        assert hasattr(resp, "data"), "Response should have a 'data' attribute"
        print(
            f"\n[live] list_vms returned {len(resp.data or [])} VMs "
            f"(total_available={getattr(resp.metadata, 'total_available_results', 'N/A')})"
        )

    def test_custom_headers_present_on_client(self):
        """Verify CF Access headers are set on the API client before any request."""
        cf_id = os.environ.get("NUTANIX_HEADER_CF_ACCESS_CLIENT_ID")
        cf_secret = os.environ.get("NUTANIX_HEADER_CF_ACCESS_CLIENT_SECRET")
        if not cf_id or not cf_secret:
            pytest.skip("CF Access env vars not set — skipping header presence check")

        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.vmm.api_client import (
            get_api_client,
        )

        module = self._build_module()
        client = get_api_client(module)

        default_headers = getattr(client, "_ApiClient__default_headers", {})
        assert (
            "Cf-Access-Client-Id" in default_headers
        ), "CF-Access-Client-Id header missing from API client default headers"
        assert (
            "Cf-Access-Client-Secret" in default_headers
        ), "CF-Access-Client-Secret header missing from API client default headers"
        assert default_headers["Cf-Access-Client-Id"] == cf_id
        assert default_headers["Cf-Access-Client-Secret"] == cf_secret
        print("\n[live] CF Access headers confirmed on API client")

    def test_list_vms_with_filter(self):
        """list_vms() with an OData filter returns only matching VMs."""
        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.vmm.api_client import (
            get_vm_api_instance,
        )

        module = self._build_module()
        vmm = get_vm_api_instance(module)

        resp = vmm.list_vms(_page=0, _limit=10, _filter="startswith(name, 'frg-')")

        assert resp is not None
        assert hasattr(resp, "data")
        vms = resp.data or []
        print(f"\n[live] list_vms(filter='frg-') returned {len(vms)} VMs")
        for vm in vms:
            vm_dict = vm.to_dict() if hasattr(vm, "to_dict") else {}
            assert vm_dict.get("name", "").startswith(
                "frg-"
            ), f"VM '{vm_dict.get('name')}' does not match filter startswith(name, 'frg-')"

    def test_inventory_plugin_parse_returns_hosts(self):
        """Full end-to-end: InventoryModule.parse() populates hosts via the
        same code path that ansible-inventory --graph uses."""
        from unittest.mock import patch as mock_patch

        from ansible.inventory.data import InventoryData
        from ansible.parsing.dataloader import DataLoader
        from ansible_collections.nutanix.ncp.plugins.inventory.ntnx_prism_vm_inventory_v2 import (
            InventoryModule,
        )

        inventory = InventoryData()
        loader = DataLoader()

        options = {
            "nutanix_host": os.environ.get("NUTANIX_HOST"),
            "nutanix_port": os.environ.get("NUTANIX_PORT", "9440"),
            "nutanix_username": None,
            "nutanix_password": None,
            "nutanix_api_key": os.environ.get("NUTANIX_API_KEY"),
            "custom_headers": None,
            "validate_certs": False,
            "fetch_all_vms": False,
            "page": 0,
            "limit": 10,
            "filter": None,
            "custom_ansible_host": None,
            "nutanix_debug": False,
            "nutanix_log_file": None,
            "filters": [],
            "strict": False,
            "compose": {},
            "groups": {},
            "keyed_groups": [],
        }

        plugin = InventoryModule()

        # Patch _read_config_data to a no-op and inject options directly,
        # bypassing Ansible's config manager (not available outside ansible-test).
        with mock_patch.object(InventoryModule, "_read_config_data"):
            plugin._options = options
            plugin.parse(inventory, loader, "nutanix.yaml", cache=False)

        hosts = list(inventory.hosts.keys())
        print(f"\n[live] inventory parse() added {len(hosts)} hosts: {hosts[:5]}")
        assert len(hosts) > 0, "Expected at least one host from inventory parse()"
