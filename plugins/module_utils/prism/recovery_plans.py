# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from ..prism.vms import get_vm_uuid
from .prism import Prism

__metaclass__ = type


class RecoveryPlan(Prism):
    def __init__(self, module):
        resource_type = "/recovery_plans"
        super(RecoveryPlan, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "primary_location": self._build_spec_primary_location,
            "recovery_location": self._build_spec_recovery_location,
            "stages": self._build_spec_stages,
            "network_mappings": self._build_spec_network_mappings
        }

    def get_associated_entities(self, recovery_plan_uuid):
        return self.read(uuid=recovery_plan_uuid, endpoint="entities")

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "recovery_plan"},
                "spec": {
                    "resources": {
                        "parameters": {
                            "network_mapping_list": [],
                            "availability_zone_list": [
                                {}, {}
                            ],
                            "primary_location_index": 0
                        },
                        "stage_list": [],
                    }, 
                    "name": None
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None
    
    def _build_spec_stages(self, payload, stages):
        stage_list = []
        for stage in stages:
            stage_spec = {}
            stage_entities = []
            for vm in stages.get("vms", []):
                uuid, err = get_vm_uuid(vm, self.module)
                if err:
                    return None, err
                vm_spec = {
                    "any_entity_reference":{
                        "kind": "vm",
                        "uuid": uuid
                    }
                }
                if vm.get("enable_script_exec"):
                    vm_spec["script_list"] = [
                        {
                            "enable_script_exec": vm["enable_script_exec"]
                        }
                    ]
                stage_entities.append(vm_spec)

            for category in stages.get("categories"):
                category_spec = {
                    "categories": {
                        category["key"]: category["value"]
                    }
                }
                if category.get("enable_script_exec"):
                    category_spec["script_list"] = [
                        {
                            "enable_script_exec": category["enable_script_exec"]
                        }
                    ]
                stage_entities.append(category_spec)
            stage_spec["stage_work"]["recover_entities"]["entity_info_list"] = stage_entities
            if stage.get("delay"):
                stage_spec["delay"] = stage["delay"]
            stage_list.append(stage_spec)
        payload["spec"]["resources"]["stage_list"] = stage_list
        return payload, None

    def _build_spec_network_mappings(self, payload, network_mappings):
        network_mappings = []

        # apply this settings to all network mappings
        are_network_stretched = False
        if self.moudule.params["network_type"] == "STRETCH":
            are_network_stretched = True

        # create primary and recovery location spec to be used in each network mappings
        primary_location = {}
        recovery_location = {}
        if self.module.params.get("primary_location", {}).get("url"):
            primary_location = {
                "availability_zone_url": self.module.params["primary_location"]["url"]
            }
            if self.module.params["primary_location"].get("cluster"):
                primary_location["cluster_reference_list"] = [
                    {
                        "uuid": self.module.params["primary_location"]["cluster"]
                    }
                ]
        else:
            primary_location_index = payload["spec"]["resources"]["parameters"]["primary_location_index"]
            primary_location = payload["spec"]["resources"]["parameters"]["availability_zone_list"][primary_location_index]
        
        if self.module.params.get("recovery_location", {}).get("url"):
            recovery_location = {
                "availability_zone_url": self.module.params["recovery_location"]["url"]
            }
            if self.module.params["recovery_location"].get("cluster"):
                recovery_location["cluster_reference_list"] = [
                    {
                        "uuid": self.module.params["recovery_location"]["cluster"]
                    }
                ]
        else:
            recovery_location_index = payload["spec"]["resources"]["parameters"]["primary_location_index"] ^ 1
            recovery_location = payload["spec"]["resources"]["parameters"]["availability_zone_list"][recovery_location_index]
        
        for ntw in network_mappings:
            spec = {}
            primary_ntw_spec = {}
            recovery_ntw_spec = {}
            if ntw["primary"].get("test"):
                subnet_spec = deepcopy(ntw["primary"]["test"])
                primary_ntw_spec["test_network"] = {
                    "name": ntw["primary"]["test"]["name"], 
                    "subnet_list": [subnet_spec.pop("name")]
                }

            if ntw["primary"].get("prod"):
                subnet_spec = deepcopy(ntw["primary"]["prod"])
                primary_ntw_spec["recovery_network"] = {
                    "name": ntw["primary"]["prod"]["name"], 
                    "subnet_list": [subnet_spec.pop("name")]
                }
            
            if ntw["recovery"].get("test"):
                subnet_spec = deepcopy(ntw["recovery"]["test"])
                recovery_ntw_spec["test_network"] = {
                    "name": ntw["recovery"]["test"]["name"], 
                    "subnet_list": [subnet_spec.pop("name")]
                }
            
            if ntw["recovery"].get("prod"):
                subnet_spec = deepcopy(ntw["recovery"]["prod"])
                recovery_ntw_spec["recovery_network"] = {
                    "name": ntw["recovery"]["prod"]["name"], 
                    "subnet_list": [subnet_spec.pop("name")]
                }
                
            
            primary_ntw_spec.update(primary_location)
            recovery_ntw_spec.update(recovery_location)

            spec["are_networks_stretched"]=are_network_stretched  
            spec["availability_zone_network_mapping_list"] = [primary_ntw_spec, recovery_ntw_spec]
            network_mappings.append(spec)

        payload["spec"]["resources"]["parameters"]["network_mapping_list"] = network_mappings
        return payload, None

    def _build_spec_primary_location(self, payload, primary_location):
        primary_location_index = payload["spec"]["resources"]["parameters"]["primary_location_index"]
        spec = {
            "availability_zone_url": primary_location["url"]
        }
        if primary_location.get("cluster"):
            spec["cluster_reference_list"] = [
                {
                    "uuid": primary_location["cluster"]
                }
            ]
        payload["spec"]["resources"]["parameters"]["availability_zone_list"][primary_location_index] = spec
        return payload, None

    def _build_spec_recovery_location(self, payload, recovery_location):
        recovery_location_index = payload["spec"]["resources"]["parameters"]["primary_location_index"] ^ 1
        spec = {
            "availability_zone_url": recovery_location["url"]
        }
        if recovery_location.get("cluster"):
            spec["cluster_reference_list"] = [
                {
                    "uuid": recovery_location["cluster"]
                }
            ]
        payload["spec"]["resources"]["parameters"]["availability_zone_list"][recovery_location_index] = spec
        return payload, None