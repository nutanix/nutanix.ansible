#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_content_repository_items_info_v2
short_description: List content repository items from Nutanix Prism Central using v4 APIs
version_added: "2.7.0"
description:
    - This module lists items belonging to a content repository.
    - Supports pagination, filtering, ordering, and select query parameters.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(View Content Repository Item) -
      Required Roles: Account Owner, Administrator, Consumer, CSI System, Developer, Kubernetes Data Services System,
      Kubernetes Infrastructure Provision, Multidomain Admin, Multidomain Viewer, NCM Connector, Prism Admin, Prism Viewer,
      Project Admin, Project Manager, Super Admin, User, Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=multidomain)"
options:
    ext_id:
        description:
            - External identifier of the content repository whose items should be listed.
        type: str
        required: true
    cluster_ext_id:
        description:
            - External identifier of a Domain Manager or Prism Central.
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
- name: List all items in a content repository
  nutanix.ncp.ntnx_content_repository_items_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
  register: result

- name: List content repository items with filter
  nutanix.ncp.ntnx_content_repository_items_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
    filter: "name eq 'centos-image'"
  register: result

- name: List content repository items with limit
  nutanix.ncp.ntnx_content_repository_items_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
    limit: 5
  register: result
"""

RETURN = r"""
response:
    description:
        - List of content repository items.
    returned: always
    type: list
    sample: [
            {
                "create_time": "2026-09-21T08:00:00.000000+00:00",
                "description": null,
                "ext_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "last_update_time": "2026-09-21T08:00:00.000000+00:00",
                "links": null,
                "name": "centos-image",
                "owner_ext_id": "00000000-0000-0000-0000-000000000000",
                "size_bytes": 262472192,
                "state": "READY",
                "tenant_id": null,
                "type": "IMAGE",
            },
        ]

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the content repository.
    type: str
    returned: always
    sample: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str

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
        - The total number of available items in the content repository.
    type: int
    returned: always
    sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_content_repositories_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str"),
    )
    return module_args


def list_content_repository_items(module, content_repositories, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating content repository items info spec", **result
        )

    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    try:
        resp = content_repositories.list_content_repository_items_by_content_repository_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing content repository items",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None, "ext_id": None}

    content_repositories = get_content_repositories_api_instance(module)
    list_content_repository_items(module, content_repositories, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
