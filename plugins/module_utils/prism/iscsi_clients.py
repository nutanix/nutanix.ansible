# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy


class Clients:
    @classmethod
    def get_spec(cls, iscsi_client, chap_auth=False):
        payload = cls._get_default_spec()
        spec, error = cls._build_spec_iscsi_client(payload, iscsi_client, chap_auth)
        if error:
            return None, error
        return spec, None

    @staticmethod
    def _get_default_spec():
        return deepcopy({"enabledAuthentications": "NONE"})

    @staticmethod
    def _build_spec_iscsi_client(payload, iscsi_client, chap_auth):

        if iscsi_client.get("uuid"):
            payload["extId"] = iscsi_client["uuid"]
        elif iscsi_client.get("iscsi_iqn"):
            payload["iscsiInitiatorName"] = iscsi_client["iscsi_iqn"]
        elif iscsi_client.get("iscsi_ip"):
            payload["iscsiInitiatorNetworkId"] = {
                "$objectType": "common.v1.config.IPAddressOrFQDN",
                "$reserved": {
                    "$fqObjectType": "common.v1.r0.a3.config.IPAddressOrFQDN"
                },
                "$unknownFields": {},
                "ipv4": {
                    "$objectType": "common.v1.config.IPv4Address",
                    "$reserved": {
                        "$fqObjectType": "common.v1.r0.a3.config.IPv4Address"
                    },
                    "$unknownFields": {},
                    "value": iscsi_client["iscsi_ip"],
                },
            }
        if chap_auth and iscsi_client.get("client_password"):
            payload["clientSecret"] = iscsi_client["client_password"]

            payload["enabledAuthentications"] = "CHAP"

        return payload, None
