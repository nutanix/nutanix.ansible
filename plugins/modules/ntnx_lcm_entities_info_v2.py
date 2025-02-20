#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_entities_info_v2
short_description: Fetch LCM Entities Info
description:
    - This module fetches LCM Entities Info.
    - Fetch a particular LCM entity details using external ID.
version_added: 2.0.0
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options:
    ext_id:
        description:
            - The external ID of the entity.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch LCM entity using external ID
  nutanix.ncp.ntnx_lcm_entities_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "3c196eac-e1d5-1b8a-9b01-c133f6907ca2"
  register: lcm_entity
"""

RETURN = r"""
response:
    description: The response from the LCM config API
    type: dict
    returned: always
    sample:
        {
            "available_versions": [
                {
                    "available_version_uuid": "f8d6b44a-590d-4116-b19d-32d9b393d690",
                    "child_entities": null,
                    "custom_message": null,
                    "dependencies": null,
                    "disablement_reason": null,
                    "group_uuid": null,
                    "is_enabled": null,
                    "order": 15,
                    "release_date": null,
                    "release_notes": null,
                    "status": "AVAILABLE",
                    "version": "4.0.0"
                }
            ],
            "child_entities": null,
            "cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055",
            "device_id": null,
            "entity_class": "PC CORE CLUSTER",
            "entity_description": null,
            "entity_details": null,
            "entity_model": "Calm Policy Engine",
            "entity_type": "SOFTWARE",
            "entity_version": "3.8.0",
            "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
            "group_uuid": null,
            "hardware_family": null,
            "hardware_vendor": null,
            "last_updated_time": "2025-02-16T09:56:57.131022+00:00",
            "links": null,
            "location_info": {
                "location_type": "PC",
                "uuid": "1e9a1996-50e2-485f-a67c-22355cb43055"
            },
            "sub_entities": null,
            "target_version": "3.8.0",
            "tenant_id": null
        }
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_entity_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_entity  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_entity_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_entity(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_entities(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed to generate info spec for entities", **result)

    try:
        resp = api_instance.list_entities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM entities info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }

    api_instance = get_entity_api_instance(module)
    if module.params.get("ext_id"):
        get_entity_using_ext_id(module, api_instance, result)
    else:
        get_entities(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
