#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_projects_info_v2
short_description: Fetch projects info from Nutanix Prism Central using v4 APIs
version_added: "2.6.0"
description:
    - This module fetches information about Nutanix projects.
    - The module can fetch information about all projects or a specific project.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - The external ID of the project.
            - If provided, fetches a single project.
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
- name: List all projects
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get project by external ID
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

- name: List projects with limit
  nutanix.ncp.ntnx_projects_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Projects info v4 API.
        - It can be a single project if external ID is provided.
        - List of multiple projects if external ID is not provided.
    returned: always
    type: dict
    sample: "<Need to add sample>"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

ext_id:
    description:
        - The external ID of the project when a specific project is fetched.
    type: str
    returned: When a single entity is fetched
    sample: "00000000-0000-0000-0000-000000000000"

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching projects info"

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true

total_available_results:
    description:
        - The total number of available projects in PC.
    type: int
    returned: When all projects are fetched
    sample: 10
"""

import warnings  # noqa: E402

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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_project_by_ext_id(module, projects, result):
    ext_id = module.params.get("ext_id")

    resp = get_project(module, projects, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_projects(module, projects, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating projects info spec", **result)

    try:
        resp = projects.list_projects(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching projects info",
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
    result = {"changed": False, "response": None}

    projects = get_projects_api_instance(module)

    if module.params.get("ext_id"):
        get_project_by_ext_id(module, projects, result)
    else:
        get_projects(module, projects, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
