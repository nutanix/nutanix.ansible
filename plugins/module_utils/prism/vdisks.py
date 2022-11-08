# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .groups import get_entity_uuid


class VDisks:
    @classmethod
    def get_spec(cls, module, vdisk):
        payload = cls._get_default_spec()
        spec, error = cls._build_spec_vdisk(module, payload, vdisk)
        if error:
            return None, error
        return spec, None

    @staticmethod
    def _get_default_spec():
        return deepcopy(
            {
                "diskSizeBytes": None,
            }
        )

    @staticmethod
    def _build_spec_vdisk(module, payload, vdisk):

        disk_size_bytes = vdisk["size_gb"] * 1024 * 1024 * 1024

        payload["diskSizeBytes"] = disk_size_bytes

        if vdisk.get("storage_container"):
            uuid, error = get_entity_uuid(
                vdisk["storage_container"],
                module,
                key="container_name",
                entity_type="storage_container",
            )
            if error:
                return None, error

            payload["diskDataSourceReference"] = (
                {
                    "$objectType": "common.v1.config.EntityReference",
                    "$reserved": {
                        "$fqObjectType": "common.v1.r0.a3.config.EntityReference"
                    },
                    "$unknownFields": {},
                    "extId": uuid,
                    "entityType": "STORAGE_CONTAINER",
                },
            )
        elif vdisk.get("uuid"):
            payload["extId"] = vdisk["uuid"]

        return payload, None
