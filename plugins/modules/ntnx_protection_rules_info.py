#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_protection_rules_info
short_description: protection rule info module
version_added: 1.5.0
description: 'Get protection rule  info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: protection_rule
    rule_uuid:
        description:
            - protection rule UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""

- name: List all Protection rules
  ntnx_protection_rules_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
  register: result
  ignore_errors: True

- name: List protection rule using uuid criteria
  ntnx_protection_rules_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    rule_uuid: "{{ test_rule_uuid }}"
  register: result

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
        "rule_info": resp,
        "rule_affected_entities": affected_entities,
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
