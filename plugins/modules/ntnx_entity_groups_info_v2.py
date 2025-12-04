#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_groups_info_v2
short_description: Get entity groups info
version_added: 2.0.0
description:
    - Fetch specific entity group info using external ID
    - Fetch list of multiple entity groups info if external ID is not provided with optional filters
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID to fetch specific entity group info
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
  description:
      - Response for fetching entity groups info
      - One entity group info if External ID is provided
      - List of multiple entity groups info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
        "allowed_config": {
            "entities": [
                {
                    "kube_entities": null,
                    "reference_ext_ids": [
                        "83c8be14-a656-4a53-6e2c-84d0e6b84182",
                        "6742b519-b958-4638-679c-c7b2d151c44a"
                    ],
                    "select_by": "CATEGORY_EXT_ID",
                    "type": "SUBNET"
                }
            ]
        },
        "description": "mkWyftswwhuhansible-eg2_entity_group_desc",
        "ext_id": "f56fb070-c59e-47bf-bb43-657854189abd",
        "links": null,
        "name": "mkWyftswwhuhansible-eg2_entity_group",
        "owner_ext_id": "00000000-0000-0000-0000-000000000000",
        "policy_ext_ids": null,
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching entity groups info"

total_available_results:
    description:
        - The total number of available entity groups in PC.
    type: int
    returned: when all entity groups are fetched
    sample: 125
"""
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_entity_groups_api_instance,
)
from ..module_utils.v4.flow.helpers import get_entity_group  # noqa: E402
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


def get_entity_group_using_ext_id(module, entity_groups, result):
    ext_id = module.params.get("ext_id")
    resp = get_entity_group(module, entity_groups, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_entity_groups(module, entity_groups, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating entity groups info Spec", **result)

    try:
        resp = entity_groups.list_entity_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entity groups info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    entity_groups = get_entity_groups_api_instance(module)
    if module.params.get("ext_id"):
        get_entity_group_using_ext_id(module, entity_groups, result)
    else:
        get_entity_groups(module, entity_groups, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
