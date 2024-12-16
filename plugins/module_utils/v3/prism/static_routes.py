# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .subnets import get_subnet_uuid
from .vpcs import Vpc
from .vpn_connections import get_vpn_connection_uuid


class StaticRoute(Vpc):
    default_route_dest = "0.0.0.0/0"
    route_tables_endpoint = "route_tables"

    def __init__(self, module):
        super(StaticRoute, self).__init__(module)
        self.build_spec_methods = {
            "static_routes": self._build_spec_static_routes,
            "remove_all_routes": self._build_spec_remove_all_routes,
        }

    def update_static_routes(self, data, vpc_uuid):
        return self.update(
            data=data, uuid=vpc_uuid, endpoint=self.route_tables_endpoint
        )

    def get_static_routes(self, vpc_uuid):
        return self.read(uuid=vpc_uuid, endpoint=self.route_tables_endpoint)

    def _get_default_spec(self):
        return deepcopy(
            {
                "metadata": {"kind": "vpc_route_table"},
                "spec": {
                    "resources": {
                        "static_routes_list": [],
                        "default_route_nexthop": None,
                    }
                },
            }
        )

    def _build_default_route_spec(self, payload, next_hop):
        if payload["spec"]["resources"].get("default_route_nexthop"):
            error = "More than one default routes are not allowed"
            return None, error
        payload["spec"]["resources"]["default_route_nexthop"] = next_hop
        return payload, None

    def _build_spec_static_routes(self, payload, inp_static_routes):
        # since static route list has to be overriden
        if payload["spec"]["resources"].get("default_route_nexthop"):
            payload["spec"]["resources"].pop("default_route_nexthop")
        static_routes_list = []
        for route in inp_static_routes:
            next_hop = {}
            if route["next_hop"].get("external_subnet_ref"):
                subnet_ref = route["next_hop"]["external_subnet_ref"]
                uuid, err = get_subnet_uuid(subnet_ref, self.module)
                if err:
                    return None, err
                next_hop["external_subnet_reference"] = {"kind": "subnet", "uuid": uuid}
            elif route["next_hop"].get("vpn_connection_ref"):
                vpn_ref = route["next_hop"]["vpn_connection_ref"]
                uuid, err = get_vpn_connection_uuid(self.module, vpn_ref)
                if err:
                    return None, err
                next_hop["vpn_connection_reference"] = {
                    "kind": "vpn_connection",
                    "uuid": uuid,
                }

            if route["destination"] == self.default_route_dest:
                default_spec, err = self._build_default_route_spec(payload, next_hop)
                if err:
                    return None, err
            else:
                static_routes_list.append(
                    {"nexthop": next_hop, "destination": route["destination"]}
                )

        payload["spec"]["resources"]["static_routes_list"] = static_routes_list
        return payload, None

    def _build_spec_remove_all_routes(self, payload, remove_all_routes):
        if remove_all_routes:
            if payload["spec"]["resources"].get("default_route_nexthop"):
                payload["spec"]["resources"].pop("default_route_nexthop")
            payload["spec"]["resources"]["static_routes_list"] = []
        return payload, None
