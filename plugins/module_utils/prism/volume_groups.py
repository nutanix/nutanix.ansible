# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .clusters import get_cluster_uuid
from .prism import Prism
from .vms import get_vm_uuid


class VolumeGroup(Prism):
    __BASEURL__ = "/api/storage/v4.0.a2/config"

    def __init__(self, module):
        resource_type = "/volume-groups"
        super(VolumeGroup, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "cluster": self._build_spec_cluster,
            "target_prefix": self._build_spec_target_prefix,
            "load_balance": self._build_spec_load_balance,
            "flash_mode": self._build_spec_flash_mode,
        }

    # def get_uuid(self, value, key="name", raise_error=True, no_response=False):
    #     data = {"filter": "{0}=={1}".format(key, value)}
    #     resp = self.list(data, raise_error=raise_error, no_response=no_response)
    #     entities = resp.get("entities") if resp else None
    #     if entities:
    #         for entity in entities:
    #             if entity["service_group"]["name"] == value:
    #                 return entity["uuid"]
    #     return None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "loadBalanceVmAttachments": False,
                "sharingStatus": "SHARED",
                "clusterReference": None,
                "usageType": "USER",
            }
        )

    def _build_spec_name(self, payload, value):
        payload["name"] = value
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["description"] = value
        return payload, None

    def _build_spec_target_prefix(self, payload, value):
        payload["iscsiTargetPrefix"] = value
        return payload, None

    def _build_spec_load_balance(self, payload, value):
        payload["loadBalanceVmAttachments"] = value
        return payload, None

    def _build_spec_flash_mode(self, payload, value):
        payload["storageFeatures"] = {
            "$objectType": "storage.v4.config.StorageFeatures",
            "$reserved": {"$fqObjectType": "storage.v4.r0.a2.config.StorageFeatures"},
            "$unknownFields": {},
            "flashMode": {
                "$objectType": "storage.v4.config.FlashMode",
                "$reserved": {"$fqObjectType": "storage.v4.r0.a2.config.FlashMode"},
                "$unknownFields": {},
                "isEnabled": True,
            },
        }
        return payload, None

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(param, self.module)
        if err:
            return None, err
        payload["clusterReference"] = uuid
        return payload, None

    def get_vm_spec(self, vm):
        uuid, error = get_vm_uuid(vm, self.module)
        if error:
            return None, error
        spec = {"extId": uuid}
        return spec, None

    def get_client_spec(self, client):
        # uuid, error = get_client_uuid(client, self.module)
        # if error:
        #     return None, error
        spec = {"extId": client["uuid"]}
        return spec, None


# Helper functions


def get_volume_group_uuid(config, module):
    if "name" in config:
        service_group = VolumeGroup(module)
        name = config["name"]
        uuid = service_group.get_uuid(name)
        if not uuid:
            error = "Volume Group {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
