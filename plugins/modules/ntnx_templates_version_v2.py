#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_version_v2
short_description: Manage Nutanix template versions
description:
    - This module allows you to publish or delete template versions in Nutanix.
    - This module uses PC v4 APIs based SDKs
version_added: '2.0.0'
options:
    template_ext_id:
        description:
            - The unique identifier of the template.
        required: true
        type: str
    version_id:
        description:
            - The unique identifier of the template version.
        required: true
        type: str
    state:
        description:
            - The desired state of the template version.
            - If set to "present", the template version will be published.
            - If set to "absent", the template version will be deleted.
        choices: ['present', 'absent']
    wait:
        description:
            - Whether to wait for the task to complete before returning.
        required: false
        type: bool
        default: True
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Set the Active Version
  nutanix.ncp.ntnx_templates_version_v2:
    template_ext_id: "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64"
    version_id: "5fbfc4d6-7736-49e4-97e7-eb55b061f16f"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Delete Template Version
  nutanix.ncp.ntnx_templates_version_v2:
    state: absent
    template_ext_id: "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64"
    version_id: "5fbfc4d6-7736-49e4-97e7-eb55b061f16f"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""

RETURN = r"""
response:
    description: The response from the Nutanix API.
    type: dict
    returned: always
    sample: {
        "ext_id": "task-789",
        "status": "Succeeded"
    }
task_ext_id:
    description: The unique identifier of the task.
    type: str
    returned: always
    sample: "task-789"
changed:
    description: Indicates whether the state of the template version was changed.
    type: bool
    returned: always
    sample: true
error:
    description: The error message, if any.
    type: str
    returned: on failure
    sample: "Failed to publish template version"
template_ext_id:
    description: The unique identifier of the template.
    type: str
    returned: always
    sample: "f3ae7dfe-9f7f-4085-8619-5d93ad9c4e64"
ext_id:
    description: The unique identifier of the template version.
    type: str
    returned: always
    sample: "5fbfc4d6-7736-49e4-97e7-eb55b061f16f"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        template_ext_id=dict(type="str", required=True),
        version_id=dict(type="str", required=True),
    )

    return module_args


def publish_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("template_ext_id")
    result["template_ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for publish template version", **result
        )

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
        return

    kwargs = {"if_match": etag}

    try:
        resp = templates.publish_template(extId=ext_id, body=spec, **kwargs)
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
        resp = get_template(module, templates, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_template_version(module, result):
    templates = get_templates_api_instance(module)
    template_ext_id = module.params.get("template_ext_id")
    ext_id = module.params.get("version_id")
    result["template_ext_id"] = template_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Template version with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_template(module, templates, template_ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting template version", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = templates.delete_template_version_by_id(
            templateExtId=template_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting template version",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
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
    }
    state = module.params["state"]
    if state == "present":
        publish_template(module, result)
    else:
        delete_template_version(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
