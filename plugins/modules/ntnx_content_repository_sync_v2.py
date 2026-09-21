#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_content_repository_sync_v2
short_description: Sync items of a subscribed content repository using v4 APIs
version_added: "2.7.0"
description:
    - Sync items of a subscribed content repository from its source.
    - The source and target Prism Central domains must be connected through an Availability Zone registration.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Sync Content Repository) -
      Required Roles: Account Owner, Administrator, Multidomain Admin, Prism Admin, Project Admin, Project Manager,
      Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=multidomain)"
options:
    ext_id:
        description:
            - The external identifier of a subscribed Content Repository.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Sync items of a subscribed content repository
  nutanix.ncp.ntnx_content_repository_sync_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
  register: result
"""

RETURN = r"""
response:
    description:
        - Task details when C(wait) is false.
        - Content repository details when C(wait) is true.
    returned: always
    type: dict

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the content repository.
    returned: always
    type: str
    sample: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"

task_ext_id:
    description: The external ID of the task created for the operation.
    returned: always
    type: str
    sample: "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57"

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str
    sample: "Api Exception raised while syncing content repository"

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_content_repositories_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_content_repository  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def sync_content_repository(module, content_repositories, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Content repository with ext_id:{0} will be synced.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = content_repositories.sync_content_repository(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while syncing content repository",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_content_repository(module, content_repositories, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
    }

    content_repositories = get_content_repositories_api_instance(module)
    sync_content_repository(module, content_repositories, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
