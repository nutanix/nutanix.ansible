#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_projects_info
short_description: projects info module
version_added: 1.4.0
description: 'Get projects info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: project
    project_uuid:
        description:
            - project UUID
        type: str
    include_acps:
        description:
            - set it to include acps in response while getting project using uuid
        type: bool
        default: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: List project using name filter criteria
  ntnx_projects_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter:
      name: "test-ansible-project-7"

- name: List all projects
  ntnx_projects_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List project using project uuid criteria
  ntnx_projects_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    project_uuid: "<uuid>"
  register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description:
    - Metadata for project list output using uuid
    - Below response is when we use project_uuid for getting info
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-07-15T10:59:25Z",
                "kind": "project",
                "last_update_time": "2022-07-15T10:59:26Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "project_reference": {
                    "kind": "project",
                    "name": "integration_test_project",
                    "uuid": "csb38ebbf-de15-4239-8197-cedcf27ec88d"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 0,
                "uuid": "csb38ebbf-de15-4239-8197-cedcf27ec88d"
            }
spec:
  description:
    - given project spec response
    - below response is when we use project_uuid for getting info
  returned: always
  type: dict
  sample: {
                "name": "integration_test_project",
                "resources": {
                    "external_user_group_reference_list": [],
                    "subnet_reference_list": [
                        {
                            "kind": "subnet",
                            "uuid": "f1c7a142-ed69-4077-9385-ee34dd6a3532"
                        }
                    ],
                    "user_reference_list": []
                }
            }
status:
  description:
    - given project status response
    - below response is when we use project_uuid for getting info
  returned: always
  type: dict
  sample:  {
                "description": "",
                "execution_context": {
                    "task_uuid": [
                        "2ad6sea7-9739-4fe9-97cc-87acb67341d7"
                    ]
                },
                "name": "integration_test_project",
                "resources": {
                    "account_reference_list": [],
                    "cluster_reference_list": [],
                    "environment_reference_list": [],
                    "external_network_list": [],
                    "external_user_group_reference_list": [],
                    "is_default": false,
                    "resource_domain": {
                        "resources": []
                    },
                    "subnet_reference_list": [
                        {
                            "kind": "subnet",
                            "name": "xx-xxx",
                            "uuid": "f1b7c142-ed69-4077-9385-ee34dd6a3532"
                        }
                    ],
                    "tunnel_reference_list": [],
                    "user_reference_list": [],
                    "vpc_reference_list": []
                },
                "state": "COMPLETE"
            }
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v3.prism.projects import Project  # noqa: E402
from ..module_utils.v3.prism.projects_internal import ProjectsInternal  # noqa: E402


def get_module_spec():

    module_args = dict(
        project_uuid=dict(type="str"),
        kind=dict(type="str", default="project"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
        include_acps=dict(type="bool", default=False),
    )

    return module_args


def get_project(module, result):
    projects = Project(module)
    uuid = module.params.get("project_uuid")
    resp = projects.read(uuid)
    result["response"] = resp
    if module.params.get("include_acps", False):
        _projects = ProjectsInternal(module)
        resp = _projects.read(uuid)
        result["response"]["acps"] = resp["spec"]["access_control_policy_list"]


def get_projects(module, result):
    projects = Project(module)
    spec, err = projects.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating projects info Spec", **result)
    resp = projects.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("project_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("project_uuid"):
        get_project(module, result)
    else:
        get_projects(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
