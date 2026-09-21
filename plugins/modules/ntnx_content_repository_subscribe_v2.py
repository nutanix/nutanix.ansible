#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_content_repository_subscribe_v2
short_description: Subscribe to a source content repository using v4 APIs
version_added: "2.7.0"
description:
    - Subscribe to a source content repository in a paired Prism Central domain.
    - The source and target Prism Central domains must be connected through an Availability Zone registration.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Subscribe Content Repository) -
      Required Roles: Account Owner, Administrator, Multidomain Admin, Prism Admin, Project Admin, Project Manager,
      Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=multidomain)"
options:
    ext_id:
        description:
            - The external identifier of a Content Repository.
        type: str
        required: true
    source_domain_manager_ext_id:
        description:
            - The external identifier of a source Domain Manager or Prism Central.
        type: str
        required: true
    project_ext_id:
        description:
            - The external identifier of the project to which the Content Repository subscription belongs.
            - The project name supplied by the subscriber must match the project name associated with the Content Repository.
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
- name: Subscribe to a source content repository
  nutanix.ncp.ntnx_content_repository_subscribe_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
    source_domain_manager_ext_id: "11111111-1111-1111-1111-111111111111"
    project_ext_id: "00000000-0000-0000-0000-000000000000"
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
    sample: "Api Exception raised while subscribing to content repository"

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_content_repositories_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_content_repository  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_multidomain_py_client as multidomain_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as multidomain_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        source_domain_manager_ext_id=dict(type="str", required=True),
        project_ext_id=dict(type="str", required=True),
    )
    return module_args


def subscribe_content_repository(module, content_repositories, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = multidomain_sdk.ContentRepositorySubscriptionSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating subscribe content repository spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = content_repositories.subscribe_content_repository(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while subscribing to content repository",
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
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_multidomain_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
    }

    content_repositories = get_content_repositories_api_instance(module)
    subscribe_content_repository(module, content_repositories, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
