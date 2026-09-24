# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible_collections.nutanix.ncp.tests.unit.compat import unittest
from ansible_collections.nutanix.ncp.tests.unit.compat.mock import MagicMock, patch
from ansible_collections.nutanix.ncp.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)


def _mock_vm_response(vms):
    """Helper to build a mocked list_vms response."""
    mock_resp = MagicMock()
    mock_resp.metadata.total_available_results = len(vms)
    # to_dict returns {"data": vms}
    mock_resp.to_dict.return_value = {"data": vms}
    mock_resp.data = vms
    return mock_resp


class TestNtnxVmsInfoV2IpFilter(ModuleTestCase):
    def setUp(self):
        super(TestNtnxVmsInfoV2IpFilter, self).setUp()
        # Common connection args
        self.common_args = {
            "nutanix_host": "10.0.0.1",
            "nutanix_username": "admin",
            "nutanix_password": "pass",
            "validate_certs": False,
        }

    def _run_with_ip(self, ip_address, vms, extra_args=None):
        """Patch get_vm_api_instance and run get_vms, return result dict."""
        args = dict(self.common_args)
        if extra_args:
            args.update(extra_args)
        if ip_address is not None:
            args["ip_address"] = ip_address

        set_module_args(args)

        # Import inside to avoid polluting
        from ansible_collections.nutanix.ncp.plugins.modules.ntnx_vms_info_v2 import (
            get_vms,
        )

        mock_api = MagicMock()
        mock_api.list_vms.return_value = _mock_vm_response(vms)

        with patch(
            "ansible_collections.nutanix.ncp.plugins.modules.ntnx_vms_info_v2.get_vm_api_instance",
            return_value=mock_api,
        ):
            # Need a module object that mimics AnsibleModule params
            # Use ModuleTestCase's mock but call get_vms directly with a dummy module
            # Create a minimal mock module
            mock_module = MagicMock()
            mock_module.params = args
            # get_vms expects module.params and uses SpecGenerator; SpecGenerator reads module.params and module.argument_spec_with_extra_keys
            # To avoid full AnsibleModule init, we patch SpecGenerator
            from ansible_collections.nutanix.ncp.plugins.module_utils.v4.spec_generator import (
                SpecGenerator,
            )

            # Build a real module via BaseInfoModule would be complex; instead mock get_info_spec to return empty kwargs
            with patch.object(SpecGenerator, "get_info_spec", return_value=({}, None)):
                result = {}
                # Call get_vms with mock_module
                # Need to ensure strip_internal_attributes works on vms dicts (it is pass-through for already stripped)
                # Patch raise_api_exception not needed
                get_vms(mock_module, result)
                return result, mock_api

    def test_learned_ipv4_match(self):
        # VM with learned_ip_addresses
        vm1 = {
            "ext_id": "1",
            "name": "vm1",
            "nics": [
                {
                    "nic_network_info": {
                        "nic_type": "NORMAL_NIC",
                        "ipv4_info": {"learned_ip_addresses": [{"value": "10.0.0.1"}]},
                        "ipv4_config": {},
                    }
                }
            ],
        }
        vm2 = {
            "ext_id": "2",
            "name": "vm2",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.2"}}
                    }
                }
            ],
        }
        result, _ = self._run_with_ip("10.0.0.1", [vm1, vm2])
        self.assertEqual(len(result["response"]), 1)
        self.assertEqual(result["response"][0]["ext_id"], "1")

    def test_configured_static_ipv4_match(self):
        vm = {
            "ext_id": "2",
            "name": "vm2",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.2"}}
                    }
                }
            ],
        }
        result, _ = self._run_with_ip("10.0.0.2", [vm])
        self.assertEqual(len(result["response"]), 1)
        self.assertEqual(result["response"][0]["ext_id"], "2")

    def test_secondary_ipv4_match(self):
        vm = {
            "ext_id": "3",
            "name": "vm3",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {
                            "secondary_ip_address_list": [
                                {"value": "10.0.0.3"},
                                {"value": "10.0.0.4"},
                            ]
                        }
                    }
                }
            ],
        }
        result, _ = self._run_with_ip("10.0.0.3", [vm])
        self.assertEqual(len(result["response"]), 1)
        result2, _ = self._run_with_ip("10.0.0.4", [vm])
        self.assertEqual(len(result2["response"]), 1)

    def test_ipv6_match(self):
        vm = {
            "ext_id": "4",
            "name": "vm4",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv6_info": {
                            "learned_ipv6_addresses": [{"value": "2001:db8::1"}]
                        }
                    }
                }
            ],
        }
        result, _ = self._run_with_ip("2001:db8::1", [vm])
        self.assertEqual(len(result["response"]), 1)

    def test_no_match_returns_empty(self):
        vm1 = {
            "ext_id": "1",
            "name": "vm1",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_info": {"learned_ip_addresses": [{"value": "10.0.0.1"}]}
                    }
                }
            ],
        }
        result, _ = self._run_with_ip("192.168.99.99", [vm1])
        self.assertEqual(len(result["response"]), 0)

    def test_no_ip_param_returns_all(self):
        vm1 = {
            "ext_id": "1",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.1"}}
                    }
                }
            ],
        }
        vm2 = {
            "ext_id": "2",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.2"}}
                    }
                }
            ],
        }
        vm3 = {"ext_id": "3", "nics": None}
        result, _ = self._run_with_ip(None, [vm1, vm2, vm3])
        self.assertEqual(len(result["response"]), 3)

    def test_nics_none_does_not_crash(self):
        vm = {"ext_id": "5", "name": "vm5", "nics": None}
        result, _ = self._run_with_ip("10.0.0.1", [vm])
        self.assertEqual(len(result["response"]), 0)

    def test_multiple_nics_handled(self):
        vm = {
            "ext_id": "6",
            "name": "vm6",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_info": {"learned_ip_addresses": [{"value": "10.0.0.5"}]}
                    }
                },
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.6"}}
                    }
                },
                {
                    "nic_network_info": {
                        "ipv4_config": {
                            "secondary_ip_address_list": [{"value": "10.0.0.7"}]
                        }
                    }
                },
            ],
        }
        for ip in ["10.0.0.5", "10.0.0.6", "10.0.0.7"]:
            result, _ = self._run_with_ip(ip, [vm])
            self.assertEqual(len(result["response"]), 1, f"failed for {ip}")
        result, _ = self._run_with_ip("10.0.0.99", [vm])
        self.assertEqual(len(result["response"]), 0)

    def test_exact_match_not_partial(self):
        vm = {
            "ext_id": "7",
            "name": "vm7",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.10"}}
                    }
                }
            ],
        }
        # Partial should not match
        result, _ = self._run_with_ip("10.0.0.1", [vm])
        self.assertEqual(len(result["response"]), 0)
        result2, _ = self._run_with_ip("10.0.0.10", [vm])
        self.assertEqual(len(result2["response"]), 1)

    def test_extract_helper_handles_missing_fields(self):
        from ansible_collections.nutanix.ncp.plugins.modules.ntnx_vms_info_v2 import (
            _extract_vm_ips,
        )

        self.assertEqual(_extract_vm_ips({"nics": None}), [])
        self.assertEqual(_extract_vm_ips({"nics": []}), [])
        self.assertEqual(_extract_vm_ips({}), [])
        self.assertEqual(_extract_vm_ips({"nics": [{"nic_network_info": None}]}), [])
        self.assertEqual(
            _extract_vm_ips(
                {
                    "nics": [
                        {
                            "nic_network_info": {
                                "nic_type": "SPAN_DESTINATION_NIC",
                                "ipv4_config": {"ip_address": {"value": "10.0.0.1"}},
                            }
                        }
                    ]
                }
            ),
            [],
        )

    def test_ext_id_and_ip_mutually_exclusive(self):
        # Test that BaseInfoModule validation fails when both ext_id and ip_address provided
        from ansible_collections.nutanix.ncp.plugins.module_utils.v4.base_info_module import (
            BaseInfoModule,
        )
        from ansible_collections.nutanix.ncp.plugins.modules.ntnx_vms_info_v2 import (
            get_module_spec,
        )

        set_module_args(
            {
                "nutanix_host": "10.0.0.1",
                "nutanix_username": "admin",
                "nutanix_password": "pass",
                "ext_id": "abc",
                "ip_address": "10.0.0.1",
            }
        )
        # BaseInfoModule should fail due to mutually_exclusive
        # It uses AnsibleModule's built-in check; our ModuleTestCase patches exit_json/fail_json
        # So we expect AnsibleFailJson
        with self.assertRaises(AnsibleFailJson):
            BaseInfoModule(
                argument_spec=get_module_spec(),
                supports_check_mode=False,
                mutually_exclusive=[("ext_id", "filter"), ("ext_id", "ip_address")],
            )

    def test_filter_and_ip_combined_client_side(self):
        # When both filter and ip_address provided, list_vms is called with _filter and result is further filtered by ip
        vm1 = {
            "ext_id": "1",
            "name": "vm1",
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.1"}}
                    }
                }
            ],
        }
        vm2 = {
            "ext_id": "2",
            "name": "vm1",  # same name but different IP
            "nics": [
                {
                    "nic_network_info": {
                        "ipv4_config": {"ip_address": {"value": "10.0.0.2"}}
                    }
                }
            ],
        }
        # Simulate that server already filtered by name eq 'vm1' and returned both vm1,vm2
        # Our client-side should then filter by ip 10.0.0.1 -> only vm1
        result, mock_api = self._run_with_ip(
            "10.0.0.1", [vm1, vm2], extra_args={"filter": "name eq 'vm1'"}
        )
        self.assertEqual(len(result["response"]), 1)
        self.assertEqual(result["response"][0]["ext_id"], "1")
