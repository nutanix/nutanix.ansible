# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from copy import deepcopy

from .prism import Prism


class VM(Prism):
    kind = 'vm'

    entity_type = "NutanixVm"

    def get_attr_spec(self, param, param_spec, **kwargs):
        param_method_spec = {
            "disk_list": VMDisk,
            "nic_list": VMNetwork
        }

        if param in param_method_spec:
            handler = param_method_spec[param]()
            return handler(param_spec)
        return param_spec

    def _get_api_spec(self, param_spec, **kwargs):
        pass


class VMDisk(Prism):
    entity_type = "VMDisk"

    def __init__(self):
        pass

    @staticmethod
    def get_default_spec():
        return deepcopy(
            {
                "uuid": "",
                "storage_config": {
                    "flash_mode": "",
                    "storage_container_reference": {
                        "url": "",
                        "kind": "",
                        "uuid": "",
                        "name": "",
                    },
                },
                "device_properties": {
                    "device_type": "",
                    "disk_address": {"device_index": 0, "adapter_type": ""},
                },
                "data_source_reference": {
                    "url": "",
                    "kind": "",
                    "uuid": "",
                    "name": "",
                },
                "disk_size_mib": 0,
            }
        )

    def __get_image_ref(self, name):
        pass

    def __get_storage_container_ref(self, name):
        pass

    def _get_api_spec(self, param_spec, **kwargs):

        final_disk_list = []
        _di_map = {}

        for disk_param in param_spec:
            disk_final = self.get_default_spec()
            if disk_param.get("clone_image"):
                disk_final["data_source_reference"] = self.__get_image_ref(disk_param["clone_image"])

            disk_final["device_properties"]["device_type"] = disk_param["type"]
            disk_final["device_properties"]["disk_address"]["adapter_type"] = disk_param["bus"]

            # Calculating device_index for the DISK
            if disk_param["type"] not in _di_map:
                _di_map[disk_param["type"]] = {}
            if disk_param["bus"] not in _di_map[disk_param["type"]]:
                _di_map[disk_param["type"]][disk_param["bus"]] = 0

            disk_final["device_properties"]["disk_address"]["device_index"] = _di_map[
                disk_param["type"]
            ][disk_param["bus"]]
            _di_map[disk_param["type"]][disk_param["bus"]] += 1

            # Size of disk
            disk_final["disk_size_mib"] = disk_param["size_gb"] * 1024

            if disk_param.get("storage_container"):
                disk_final["storage_config"] = {
                    "storage_container_reference": self.__get_storage_container_ref(disk_param["storage_config"])
                }
            final_disk_list.append(disk_final)
        self.remove_null_references(final_disk_list)

        return final_disk_list

    def __call__(self, param_spec, **kwargs):
        return self._get_api_spec(param_spec, **kwargs)


class VMNetwork(Prism):
    entity_type = "VMNetwork"

    def __init__(self):
        pass

    @staticmethod
    def get_default_spec():
        return deepcopy(
            {  # fill it with default value if any
                "uuid": "",
                "is_connected": False,
                "network_function_nic_type": "INGRESS",
                "nic_type": "",
                "subnet_reference": {
                    "kind": "",
                    "name": "subnet_name_default",
                    "uuid": "",
                },
                "network_function_chain_reference": "",
                "mac_address": "",
                "ip_endpoint_list": []

            }
        )

    def __get_image_ref(self, name):
        pass

    def __get_storage_container_ref(self, name):
        pass

    def _get_api_spec(self, param_spec, **kwargs):

        _di_map = {}
        final_nic_list = []
        for nic_param in param_spec:
            nic_final = self.get_default_spec()
            for k, v in nic_param.items():
                if k in nic_final.keys() and not isinstance(v, list):
                    nic_final[k] = v

                elif 'subnet_' in k and k.split('_')[-1] in nic_final['subnet_reference']:
                    nic_final['subnet_reference'][k.split('_')[-1]] = v

                elif k == "ip_endpoint_list":
                    for ip in v:
                        new_dict = {}
                        new_dict["ip"] = ip
                        nic_final[k].append(new_dict)

            final_nic_list.append(nic_final)
        self.remove_null_references(final_nic_list)

        return final_nic_list

    def __call__(self, param_spec, **kwargs):
        return self._get_api_spec(param_spec, **kwargs)
