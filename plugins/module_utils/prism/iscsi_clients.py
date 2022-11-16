# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class Clients(Prism):
    __BASEURL__ = "/api/storage/v4.0.a2/config"

    def __init__(self, module):
        resource_type = "/iscsi-clients"
        super(Clients, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {}

    def update(
            self,
            data=None,
            uuid=None,
            endpoint=None,
            query=None,
            raise_error=True,
            no_response=False,
            timeout=30,
            method="PATCH",
    ):
        resp = super(Clients, self).update(
            data,
            uuid,
            endpoint,
            query,
            raise_error,
            no_response,
            timeout,
            method,
        )
        resp["task_uuid"] = resp["data"]["extId"].split(":")[1]
        return resp

    def get_client_spec(self, iscsi_client, old_spec={}):
        payload = self._get_default_spec()
        if self.module.params.get("CHAP_auth") == "enable" or old_spec.get("enabledAuthentications"):
            chap_auth = True
        else:
            chap_auth = False

        spec, error = self._build_spec_iscsi_client(payload, iscsi_client, chap_auth)
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
        if iscsi_client.get("client_password"):
            if chap_auth:
                payload["clientSecret"] = iscsi_client["client_password"]

                payload["enabledAuthentications"] = "CHAP"
            else:
                error = "parameters are required together: CHAP_auth, client_password"
                return None, error
        return payload, None
