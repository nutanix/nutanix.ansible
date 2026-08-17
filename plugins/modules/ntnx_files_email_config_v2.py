#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_email_config_v2
short_description: Update the email configuration of a file server in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to update the email configuration of a file server in Nutanix Files.
  - The email configuration is a single (singleton) template per file server, identified by C(file_server_ext_id).
  - It defines the subject and content used by the quota-notification workflow when emailing users and administrators about quota warnings and breaches.
  - The email configuration cannot be created or deleted independently, it always exists for a file server and can only be updated.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - The state of the email configuration.
      - If C(state) is set to C(present), the email configuration of the file server is updated.
    type: str
    choices:
      - present
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server whose email configuration is updated.
      - The external ID of the file server can be fetched from Nutanix Prism Central.
    type: str
    required: true
  subject:
    description:
      - The email subject used by the quota-notification workflow.
      - If not provided, the current subject of the email configuration is retained.
    type: str
    required: false
  content:
    description:
      - The email content (body) used by the quota-notification workflow.
      - If not provided, the current content of the email configuration is retained.
    type: str
    required: false
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
- name: Update email configuration of a file server
  nutanix.ncp.ntnx_files_email_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f"
    subject: "Quota notification for your file server share"
    content: "You have exceeded the storage quota configured for your share. Please free up space."
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the email configuration of the file server.
    - It returns the updated email configuration details.
  returned: always
  type: dict
  sample:
    {
      "content": "You have exceeded the storage quota configured for your share. Please free up space.",
      "ext_id": "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f",
      "links": null,
      "subject": "Quota notification for your file server share",
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the email configuration.
  returned: always
  type: str
  sample: "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: When the operation was skipped
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, the module is idempotent or in check mode
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_quota_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_email_config  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        subject=dict(type="str"),
        content=dict(type="str"),
    )
    return module_args


def check_email_config_idempotency(current_spec, update_spec):
    return (
        current_spec.subject == update_spec.subject
        and current_spec.content == update_spec.content
    )


def update_email_config(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")

    current_spec = get_email_config(module, api_instance, file_server_ext_id)
    result["ext_id"] = current_spec.ext_id

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating email configuration", **result
        )

    # Build the update spec from the current configuration so that any attribute
    # the user does not provide retains its current value. Only the writable
    # attributes (subject and content) are carried into the request body, the
    # read-only attributes (ext_id, links, tenant_id) are intentionally omitted.
    default_spec = files_sdk.EmailConfig(
        subject=current_spec.subject, content=current_spec.content
    )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update email configuration spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_email_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_email_config(
            fileServerExtId=file_server_ext_id, body=update_spec, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating email configuration",
        )

    # The update API is synchronous and does not return the updated entity in
    # its response body, so re-fetch the email configuration to return it.
    resp = get_email_config(module, api_instance, file_server_ext_id)
    result["ext_id"] = resp.ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_quota_policies_api_instance(module)
    update_email_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
