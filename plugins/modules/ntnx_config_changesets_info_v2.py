#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_config_changesets_info_v2
short_description: Fetch config changesets info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about config changesets in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific config changeset.
    - If C(ext_id) is not provided, list multiple config changesets optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List configuration changeset(s)) -
      Required Roles: Account Owner, Administrator, NCM Admin, Nutanix Central Admin, Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin,
      User
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    ext_id:
        description:
            - The external ID of the config changeset.
            - If provided, only the config changeset with the given external ID is returned.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get config changeset using ext_id
  nutanix.ncp.ntnx_config_changesets_info_v2:
    ext_id: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  register: result
  ignore_errors: true

- name: List all config changesets
  nutanix.ncp.ntnx_config_changesets_info_v2:
  register: result
  ignore_errors: true

- name: List config changesets with filter
  nutanix.ncp.ntnx_config_changesets_info_v2:
    filter: "displayName eq 'test_entity'"
  register: result
  ignore_errors: true

- name: List config changesets with limit
  nutanix.ncp.ntnx_config_changesets_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List all config changesets with fetch_all
  nutanix.ncp.ntnx_config_changesets_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix config changesets info v4 API.
        - It can be a single config changeset if External ID is provided.
        - List of multiple config changesets if External ID is not provided with optional filter or limit.
    returned: always
    type: dict
    sample:
        {
            "changeset": {
                "display_name_changeset": {
                    "new_display_name": "new_display_name",
                    "previous_display_name": "old_display_name"
                },
                "legacy_object_list_changeset": {
                    "added_objects": [
                        "object_id_1"
                    ],
                    "removed_objects": [
                        "object_id_2"
                    ]
                },
                "legacy_operation_list_changeset": {
                    "added_operations": [
                        "op_id_1"
                    ],
                    "removed_operations": [
                        "op_id_2"
                    ]
                },
                "legacy_parent_operation_list_changeset": {
                    "added_operations": [
                        "parent_op_1"
                    ],
                    "removed_operations": [
                        "parent_op_2"
                    ]
                }
            },
            "client_name": "test_client",
            "config_type": "ENTITY",
            "created_time": "2025-01-15T10:00:00.000000+00:00",
            "display_name": "test_entity",
            "ext_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "last_updated_time": "2025-01-15T10:00:00.000000+00:00",
            "links": null,
            "tenant_id": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching config changesets info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the config changeset
    type: str
    returned: when external ID is provided
    sample: "f47ac10b-58cc-4372-a567-0e02b2c3d479"

total_available_results:
    description: The total number of available config changesets in PC.
    type: int
    returned: when all config changesets are fetched
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_config_changesets_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
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


def get_config_changeset_using_ext_id(module, config_changesets, result):
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating config changesets info spec", **result)

    kwargs["_filter"] = "extId eq '{0}'".format(ext_id)

    try:
        resp = list_entities(
            config_changesets.list_config_changesets,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching config changeset info using ext_id",
        )

    result["ext_id"] = ext_id
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        result["response"] = {}
        result["msg"] = "Config changeset with ext_id '{0}' not found".format(ext_id)
        return
    result["response"] = resp[0]


def get_config_changesets(module, config_changesets, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating config changesets info spec", **result)

    try:
        resp = list_entities(
            config_changesets.list_config_changesets,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching config changesets info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    result = {"changed": False, "response": None, "failed": False}
    config_changesets = get_config_changesets_api_instance(module)
    if module.params.get("ext_id"):
        get_config_changeset_using_ext_id(module, config_changesets, result)
    else:
        get_config_changesets(module, config_changesets, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
