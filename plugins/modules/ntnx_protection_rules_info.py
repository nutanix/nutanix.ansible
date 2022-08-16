#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.protection_rules import ProtectionRule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        rule_uuid=dict(type="str"),
        kind=dict(type="str", default="protection_rule"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params.get("rule_uuid")
    resp = protection_rule.read(rule_uuid)

    # get all affected entities
    affected_entities = protection_rule.get_affected_entities(rule_uuid)

    result["response"] = {
        "rules_info": resp,
        "rules_affected_entities": affected_entities
    }

def get_protection_rules(module, result):
    protection_rule = ProtectionRule(module)
    spec, error = protection_rule.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating protection rules info spec", **result)
    resp = protection_rule.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("rule_uuid"):
        get_protection_rule(module, result)
    else:
        get_protection_rules(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
