#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_publish_template_version_v2
short_description: Publish a template version (set the active version) in Nutanix Prism Central
version_added: 2.7.0
description:
    - Set an active version for a Nutanix VM template.
    - The active version becomes the default version used when creating VMs from
      the template and when initiating guest OS updates.
    - This module wraps the v4 C(PublishTemplate) action on C(TemplatesApi)
      (URI C(/api/vmm/v4.2/content/templates/{extId}/$actions/publish)).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Publish a template version) -
      Required Roles: Internal Super Admin, Super Admin, Prism Admin, Virtual Machine Admin,
      Tenant Admin, Project Admin, Project Manager
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported since this is an action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID of the template on which the publish action will be performed.
            - Required for the publish operation.
        type: str
        required: true
    version_id:
        description:
            - The external ID of the template version to be made the active/gold version.
            - This version will become the default for new VM deployments and guest OS updates.
            - Required for the publish operation.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Publish a template version (set the active version)
  nutanix.ncp.ntnx_publish_template_version_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64"
    version_id: "5fbfc4d6-7736-49e4-97e7-eb55b061f16f"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for publishing a template version.
        - Template details after the publish action if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "category_ext_ids": null,
            "create_time": "2026-07-21T05:13:32.104000+00:00",
            "created_by": {
                "display_name": null,
                "email_id": null,
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "first_name": null,
                "idp_id": null,
                "is_force_reset_password_enabled": null,
                "last_name": null,
                "locale": null,
                "middle_initial": null,
                "password": null,
                "region": null,
                "user_type": "LOCAL",
                "username": "admin"
            },
            "ext_id": "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64",
            "guest_update_status": null,
            "links": null,
            "template_description": "ansible test",
            "template_name": "ansible-publish-template",
            "template_version_spec": {
                "create_time": "2026-07-21T05:13:32.104000+00:00",
                "created_by": null,
                "ext_id": "5fbfc4d6-7736-49e4-97e7-eb55b061f16f",
                "is_active_version": true,
                "is_gc_override_enabled": null,
                "version_description": "Initial version",
                "version_name": "Initial Version",
                "version_source": null,
                "version_source_discriminator": null,
                "vm_spec": null
            },
            "tenant_id": null,
            "update_time": "2026-07-21T05:15:11.045000+00:00",
            "updated_by": null
        }

task_ext_id:
    description:
        - The external ID of the publish template task.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
    description:
        - The external ID of the template on which the publish action was invoked.
    returned: always
    type: str
    sample: "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

error:
    description:
        - This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Unable to fetch etag for publish template version"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while publishing template version"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_templates_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        version_id=dict(type="str", required=True),
    )
    return module_args


def publish_template_version(module, result, api_instance):
    validate_required_params(module, ["ext_id", "version_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.TemplatePublishSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating publish template version spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Template with ext_id:{0} will be published with version_id:{1}.".format(
                ext_id, module.params.get("version_id")
            )
        )
        return

    current_spec = get_template(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for publish template version", **result
        )

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.publish_template(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while publishing template version",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_template(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_templates_api_instance(module)
    publish_template_version(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
