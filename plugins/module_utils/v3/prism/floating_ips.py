# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism
from .subnets import get_subnet_uuid
from .vms import VM, get_vm_uuid
from .vpcs import get_vpc_uuid


class FloatingIP(Prism):
    def __init__(self, module):
        resource_type = "/floating_ips"
        super(FloatingIP, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "external_subnet": self._build_spec_external_subnet,
            "vm": self._build_spec_vm,
            "vpc": self._build_spec_vpc,
            "private_ip": self._build_spec_private_ip,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "floating_ip", "spec_version": 0},
                "spec": {
                    "resources": {
                        "external_subnet_reference": {"kind": "subnet", "uuid": None}
                    }
                },
            }
        )

    def _build_spec_external_subnet(self, payload, config):
        uuid, error = get_subnet_uuid(config, self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["external_subnet_reference"]["uuid"] = uuid
        return payload, None

    def _build_spec_vm(self, payload, config):
        uuid, error = get_vm_uuid(config, self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["vm_nic_reference"] = self._get_vm_nic_ref(uuid)
        return payload, None

    def _build_spec_vpc(self, payload, config):
        uuid, error = get_vpc_uuid(config, self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["vpc_reference"] = self._get_vpc_ref(uuid)
        return payload, None

    def _build_spec_private_ip(self, payload, private_ip):
        payload["spec"]["resources"]["private_ip"] = private_ip
        return payload, None

    def _get_vm_nic_ref(self, uuid):
        vm = VM(self.module)
        vm = vm.read(uuid)
        nic_list = vm["spec"]["resources"]["nic_list"]
        private_ip = self.module.params.get("private_ip")
        if len(nic_list) > 1 and private_ip:
            for nic in nic_list:
                if private_ip in nic["ip_endpoint_list"][0]:
                    uuid = nic["uuid"]
                    break
        else:
            uuid = nic_list[0]["uuid"]

        return deepcopy({"kind": "vm_nic", "uuid": uuid})

    def _get_vpc_ref(self, uuid):
        return deepcopy({"kind": "vpc", "uuid": uuid})
