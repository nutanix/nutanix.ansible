#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_content_repositories_info_v2
short_description: Fetch content repositories info from Nutanix Prism Central using v4 APIs
version_added: "2.7.0"
description:
    - This module fetches information about Nutanix content repositories.
    - The module retrieves information about a single content repository by external ID or
        lists all content repositories with optional filters and limit.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(View Content Repository) -
      Required Roles: Account Owner, Administrator, Multidomain Admin, Multidomain Viewer, Prism Admin, Prism Viewer,
      Project Admin, Project Manager, Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=multidomain)"
options:
    ext_id:
        description:
            - The external ID of the content repository.
            - If provided, fetches a single content repository.
        type: str
    cluster_ext_id:
        description:
            - External identifier of a Domain Manager or Prism Central.
        type: str
    project_ext_id:
        description:
            - External identifier of the project to which the content repository belongs.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all content repositories
  nutanix.ncp.ntnx_content_repositories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get content repository by external ID
  nutanix.ncp.ntnx_content_repositories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
  register: result

- name: List content repositories with filter
  nutanix.ncp.ntnx_content_repositories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my-content-repo'"
  register: result

- name: List content repositories with limit
  nutanix.ncp.ntnx_content_repositories_info_v2:
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
        - The response from the Nutanix PC Content Repositories info v4 API.
        - It can be a single content repository if external ID is provided.
        - List of multiple content repositories if external ID is not provided.
    returned: always
    type: dict
    sample: [
            {
                "create_time": "2026-09-21T08:00:00.000000+00:00",
                "description": "A test content repository",
                "ext_id": "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d",
                "last_update_time": "2026-09-21T08:00:00.000000+00:00",
                "links": null,
                "name": "my-content-repo",
                "owner_ext_id": "00000000-0000-0000-0000-000000000000",
                "project_ext_id": "00000000-0000-0000-0000-000000000000",
                "publisher": null,
                "state": "READY",
                "subscribers": null,
                "tenant_id": null,
                "total_item_count": 0,
            },
        ]

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

ext_id:
    description:
        - The external ID of the content repository when a specific repository is fetched.
    type: str
    returned: When a single entity is fetched
    sample: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching content repositories info"

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
        - The total number of available content repositories in PC.
    type: int
    returned: When all content repositories are fetched
    sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_content_repositories_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_content_repository  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        project_ext_id=dict(type="str"),
    )
    return module_args


def get_content_repository_by_ext_id(module, content_repositories, result):
    ext_id = module.params.get("ext_id")

    resp = get_content_repository(module, content_repositories, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_content_repositories(module, content_repositories, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating content repositories info spec", **result
        )

    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")
    if module.params.get("project_ext_id"):
        kwargs["X_Project_Id"] = module.params.get("project_ext_id")

    try:
        resp = content_repositories.list_content_repositories(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching content repositories info",
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
    result = {"changed": False, "failed": False, "response": None}

    content_repositories = get_content_repositories_api_instance(module)

    if module.params.get("ext_id"):
        get_content_repository_by_ext_id(module, content_repositories, result)
    else:
        get_content_repositories(module, content_repositories, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
