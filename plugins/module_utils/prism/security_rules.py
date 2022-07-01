# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .address_groups import get_address_uuid
from .prism import Prism
from .projects import Project
from .service_groups import get_service_uuid

__metaclass__ = type


class SecurityRule(Prism):
    def __init__(self, module):
        resource_type = "/network_security_rules"
        super(SecurityRule, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "allow_ipv6_traffic": self._build_allow_ipv6_traffic,
            "is_policy_hitlog_enabled": self._build_is_policy_hitlog_enabled,
            "vdi_rule": self._build_vdi_rule,
            "app_rule": self._build_app_rule,
            "isolation_rule": self._build_isolation_rule,
            "quarantine_rule": self._build_quarantine_rule,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "network_security_rule"},
                "spec": {
                    "name": None,
                    "resources": {"is_policy_hitlog_enabled": False},
                },
            }
        )

    def _build_spec_name(self, payload, value):
        payload["spec"]["name"] = value
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["spec"]["description"] = value
        return payload, None

    def _build_allow_ipv6_traffic(self, payload, value):
        payload["spec"]["resources"]["allow_ipv6_traffic"] = value
        return payload, None

    def _build_is_policy_hitlog_enabled(self, payload, value):
        payload["spec"]["resources"]["is_policy_hitlog_enabled"] = value
        return payload, None

    def _build_vdi_rule(self, payload, value):
        ad_rule = payload["spec"]["resources"].get("ad_rule", {})
        payload["spec"]["resources"]["ad_rule"] = self._build_spec_rule(ad_rule, value)
        return payload, None

    def _build_app_rule(self, payload, value):
        app_rule = payload["spec"]["resources"].get("app_rule", {})
        payload["spec"]["resources"]["app_rule"] = self._build_spec_rule(
            app_rule, value
        )
        return payload, None

    def _build_isolation_rule(self, payload, value):
        isolation_rule = payload["spec"]["resources"].get("isolation_rule", {})
        if not isolation_rule.get("first_entity_filter") and not isolation_rule.get(
            "second_entity_filter"
        ):
            if value.get("isolate_category"):
                isolation_rule["first_entity_filter"] = self._get_default_filter_spec()
                isolation_rule["first_entity_filter"]["params"] = value[
                    "isolate_category"
                ]

            if value.get("from_category"):
                isolation_rule["second_entity_filter"] = self._get_default_filter_spec()
                isolation_rule["second_entity_filter"]["params"] = value[
                    "from_category"
                ]
            if value.get("subset_category"):
                category_key = next(iter(value["subset_category"]))
                category_value = value["subset_category"][category_key]
                for category in isolation_rule.values():
                    if category_key in category["params"]:
                        category["params"][category_key].extend(category_value)
                    else:
                        category["params"].update(value["subset_category"])

        if value.get("policy_mode"):
            isolation_rule["action"] = value["policy_mode"]
        payload["spec"]["resources"]["isolation_rule"] = isolation_rule
        return payload, None

    def _build_quarantine_rule(self, payload, value):
        if payload["spec"]["resources"].get("quarantine_rule"):
            quarantine_rule = payload["spec"]["resources"]["quarantine_rule"]
            payload["spec"]["resources"]["quarantine_rule"] = self._build_spec_rule(
                quarantine_rule, value
            )
        return payload, None

    def _build_spec_rule(self, payload, value):
        rule = payload

        if value.get("target_group"):
            target_group = {}
            params = {}
            categories = value["target_group"].get("categories", {})
            if categories.get("adgroup"):
                params["ADGroup"] = [categories["adgroup"]]
                if value["target_group"].get("default_internal_policy"):
                    target_group["default_internal_policy"] = value["target_group"][
                        "default_internal_policy"
                    ]
            if categories.get("apptype"):
                params["AppType"] = [categories["apptype"]]
            if categories.get("apptier"):
                params["AppTier"] = [categories.get("apptier")]
                if value["target_group"].get("default_internal_policy"):
                    target_group["default_internal_policy"] = value["target_group"][
                        "default_internal_policy"
                    ]
            if categories.get("apptype_filter_by_category"):
                params.update(**categories["apptype_filter_by_category"])

            target_group["filter"] = (
                payload.get("target_group", {}).get("filter")
                or self._get_default_filter_spec()
            )
            if params:
                target_group["filter"]["params"] = params
            target_group["peer_specification_type"] = "FILTER"
            payload["target_group"] = target_group

        if value.get("inbounds"):
            rule["inbound_allow_list"] = self._generate_bound_spec(
                rule.get("inbound_allow_list", []), value["inbounds"]
            )
        elif value.get("allow_all_inbounds"):
            rule["inbound_allow_list"] = [{"peer_specification_type": "ALL"}]
        if value.get("outbounds"):
            rule["outbound_allow_list"] = self._generate_bound_spec(
                rule.get("outbound_allow_list", []), value["outbounds"]
            )
        elif value.get("allow_all_outbounds"):
            rule["outbound_allow_list"] = [{"peer_specification_type": "ALL"}]
        if value.get("policy_mode"):
            rule["action"] = value["policy_mode"]
        return rule

    def _generate_bound_spec(self, payload, list_of_rules):
        for rule in list_of_rules:
            if rule.get("rule_id"):
                rule_spec = self._filter_by_uuid(rule["rule_id"], payload)
                if rule.get("state") == "absent":
                    payload.remove(rule_spec)
                    continue
            else:
                rule_spec = {}
            if rule.get("categories"):
                rule_spec["filter"] = self._get_default_filter_spec()
                rule_spec["filter"]["params"] = rule["categories"]
                rule_spec["peer_specification_type"] = "FILTER"
            elif rule.get("ip_subnet"):
                rule_spec["ip_subnet"] = rule["ip_subnet"]
                rule_spec["peer_specification_type"] = "IP_SUBNET"
            elif rule.get("address"):
                address_group = rule["address"]

                if address_group.get("uuid"):
                    address_group["kind"] = "address_group"
                    rule_spec["address_group_inclusion_list"] = [address_group]
                elif address_group.get("name"):
                    uuid, error = get_address_uuid(address_group, self.module)
                    if error:
                        self.module.fail_json(
                            msg="Failed generating Security Rule Spec",
                            error="Entity {0} not found.".format(address_group["name"]),
                        )

                    address_group["kind"] = "address_group"
                    address_group["uuid"] = uuid
                    rule_spec["address_group_inclusion_list"] = [address_group]

                    rule_spec["peer_specification_type"] = "IP_SUBNET"

            if rule.get("protocol"):
                self._generate_protocol_spec(rule_spec, rule["protocol"])
            if rule.get("description"):
                rule_spec["description"] = rule["description"]
            if not rule_spec.get("rule_id"):
                payload.append(rule_spec)
        return payload

    def _generate_protocol_spec(self, payload, config):
        if config.get("tcp"):
            payload["protocol"] = "TCP"
            payload["tcp_port_range_list"] = config["tcp"]
        elif config.get("udp"):
            payload["protocol"] = "UDP"
            payload["udp_port_range_list"] = config["udp"]
        elif config.get("icmp"):
            payload["protocol"] = "ICMP"
            payload["icmp_type_code_list"] = config["icmp"]
        elif config.get("service"):
            service = config["service"]

            if service.get("uuid"):
                service["kind"] = "service_group"
                payload["service_group_list"] = [service]
            elif service.get("name"):
                uuid, error = get_service_uuid(service, self.module)
                if error:
                    self.module.fail_json(
                        msg="Failed generating Security Rule Spec",
                        error="Entity {0} not found.".format(service["name"]),
                    )

                service["kind"] = "service_group"
                service["uuid"] = uuid
                payload["service_group_list"] = [service]

    def _get_default_filter_spec(self):
        return deepcopy(
            {"type": "CATEGORIES_MATCH_ALL", "kind_list": ["vm"], "params": {}}
        )

    def _filter_by_uuid(self, uuid, items_list):
        try:
            return next(filter(lambda d: d.get("rule_id") == uuid, items_list))
        except BaseException:
            self.module.fail_json(
                msg="Failed generating VM Spec",
                error="Entity {0} not found.".format(uuid),
            )
