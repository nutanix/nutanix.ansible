# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
from copy import deepcopy

from .prism import Prism


class VM(Prism):
    kind = "vm"
    spec_file = "vm_spec.json"
    entity_type = "NutanixVm"

    def get_attr_spec(self, param, param_spec, **kwargs):
        param_method_spec = {"disk_list": VMDisk, "nic_list": VMNetwork}

        if param in param_method_spec:
            handler = param_method_spec[param]()
            return handler(param_spec, get_ref=self.get_entity_by_name)
        return param_spec

    def _get_api_spec(self, param_spec, **kwargs):
        pass

    def get_entity_by_name(self, name="", kind=""):
        url = self.generate_url_from_operations(kind, netloc=self.url, ops=["list"])
        data = {"filter": "name==%s" % name, "length": 1}
        resp = self.send_request(
            self.module,
            self.methods_of_actions["list"],
            url,
            data,
            self.credentials["username"],
            self.credentials["password"],
        )
        try:
            return resp["entities"][0]["metadata"]

        except IndexError:
            self.result["message"] = 'Entity with name "%s" does not exist.' % name
            self.result["failed"] = True
            self.module.exit_json(**self.result)


class VMSpec:
    def get_default_spec(self):
        raise NotImplementedError(
            "Get Default Spec helper not implemented for {0}".format(self.entity_type)
        )

    def _get_api_spec(self, param_spec, **kwargs):
        raise NotImplementedError(
            "Get Api Spec helper not implemented for {0}".format(self.entity_type)
        )

    def remove_null_references(self, spec, parent_spec=None, spec_key=None):

        if isinstance(spec, list):
            for _i in spec:
                self.remove_null_references(_i)

        elif isinstance(spec, dict):
            for _k, _v in spec.copy().items():
                if _v in [None, "", []]:
                    spec.pop(_k)
                self.remove_null_references(_v, spec, _k)

            if not bool(spec) and parent_spec and spec_key:
                parent_spec.pop(spec_key)


class VMDisk(VMSpec):
    entity_type = "VMDisk"

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
                "disk_size_mib": "",
            }
        )

    def __get_image_ref(self, name, **kwargs):
        get_entity_by_name = kwargs["get_ref"]
        entity = get_entity_by_name(name, "images")
        return {
            "kind": entity["kind"],
            "uuid": entity["uuid"],
        }

    def __get_storage_container_ref(self, name, **kwargs):
        get_entity_by_name = kwargs["get_ref"]
        entity = get_entity_by_name(name, "storage-containers")
        return {
            "kind": entity["kind"],
            "uuid": entity["uuid"],
        }

    def _get_api_spec(self, param_spec, **kwargs):

        final_disk_list = []
        _di_map = {}

        for disk_param in param_spec:
            disk_final = self.get_default_spec()
            if disk_param.get("clone_image"):
                disk_final["data_source_reference"] = self.__get_image_ref(
                    disk_param["clone_image"], **kwargs
                )

            disk_final["device_properties"]["device_type"] = disk_param["type"]
            disk_final["device_properties"]["disk_address"][
                "adapter_type"
            ] = disk_param["bus"]

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
            if disk_param.get("size_gb"):
                disk_final["disk_size_mib"] = disk_param["size_gb"] * 1024
            if disk_param.get("storage_container_name"):
                disk_final["storage_config"] = {
                    "storage_container_reference": self.__get_storage_container_ref(
                        disk_param["storage_container_name"], **kwargs
                    )
                }
            elif disk_param.get("storage_container_uuid"):
                disk_final["storage_config"] = {
                    "storage_container_reference": {
                        "kind": "storage_container",
                        "uuid": disk_param["storage_container_uuid"],
                    },
                }
            final_disk_list.append(disk_final)
        self.remove_null_references(final_disk_list)

        return final_disk_list

    def __call__(self, param_spec, **kwargs):
        return self._get_api_spec(param_spec, **kwargs)


class VMNetwork(VMSpec):
    entity_type = "VMNetwork"

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
                    "name": "",
                    "uuid": "",
                },
                "network_function_chain_reference": "",
                "mac_address": "",
                "ip_endpoint_list": [],
            }
        )

    def __get_subnet_ref(self, name, **kwargs):
        get_entity_by_name = kwargs["get_ref"]
        entity = get_entity_by_name(name, "subnets")
        return {
            "kind": entity["kind"],
            "uuid": entity["uuid"],
        }

    def _get_api_spec(self, param_spec, **kwargs):

        _di_map = {}
        final_nic_list = []
        for nic_param in param_spec:
            nic_final = self.get_default_spec()
            for k, v in nic_param.items():
                if k in nic_final.keys() and not isinstance(v, list):
                    nic_final[k] = v

                # elif 'subnet_' in k and k.split('_')[-1] in nic_final['subnet_reference']:
                #     nic_final['subnet_reference'][k.split('_')[-1]] = v

                elif k == "subnet_uuid" and v:
                    nic_final["subnet_reference"] = {"kind": "subnet", "uuid": v}
                elif k == "subnet_name" and not nic_param.get("subnet_uuid"):
                    nic_final["subnet_reference"] = self.__get_subnet_ref(v, **kwargs)

                elif k == "ip_endpoint_list" and bool(v):
                    nic_final[k] = [{"ip": v[0]}]

            final_nic_list.append(nic_final)
        self.remove_null_references(final_nic_list)

        return final_nic_list

    def __call__(self, param_spec, **kwargs):
        return self._get_api_spec(param_spec, **kwargs)
