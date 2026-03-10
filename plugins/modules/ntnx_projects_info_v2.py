#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_projects_info_v2
short_description: Fetch project information using Nutanix v4 APIs.
version_added: "2.1.0"
description:
    - Fetch information about projects from Nutanix Prism Central.
    - Retrieve a single project by external ID or list all projects with optional filters.
    - This module uses the v4 multidomain API.
options:
    ext_id:
        description:
            - The external ID of the project to retrieve.
            - Mutually exclusive with C(filter).
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get all projects
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get project by ext_id
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ project_ext_id }}"
  register: result

- name: List projects with filter
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my-project'"
  register: result

- name: List projects with pagination
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 10
    page: 0
  register: result
"""

RETURN = r"""
response:
    description:
        - The project response.
        - For a single project, this contains the project details.
        - For a list, this contains a list of project objects.
    returned: always
    type: dict or list
    sample: {
        "name": "my-project",
        "description": "A test project",
        "id": "my-project-id",
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "state": "ACTIVE",
        "is_system_defined": false,
        "is_default": false
    }
changed:
    description: Whether the state changed. Always false for info modules.
    returned: always
    type: bool
    sample: false
ext_id:
    description: The external ID of the fetched project.
    returned: when a single project is fetched
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
total_available_results:
    description: Total number of available results when listing projects.
    returned: when listing projects
    type: int
    sample: 5
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_projects_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_project  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_multidomain_py_client  # noqa: E402, F401
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_project_by_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    projects = get_projects_api_instance(module)
    resp = get_project(module, projects, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_projects(module, result):
    projects = get_projects_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list projects spec", **result)

    try:
        resp = projects.list_projects(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing projects",
        )

    resp = resp.to_dict()
    if resp.get("metadata"):
        result["total_available_results"] = resp["metadata"].get(
            "total_available_results"
        )
    result["response"] = (
        strip_internal_attributes(resp.get("data")) if resp.get("data") else []
    )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_multidomain_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    if module.params.get("ext_id"):
        get_project_by_ext_id(module, result)
    else:
        get_projects(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
