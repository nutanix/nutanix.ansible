import argparse
import os
import sys

ansible_module_content = '''#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_MNAME
short_description: MNAME module which suports INAME CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete MNAME'
options:
  nutanix_host:
    description:
      - PC hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 9440
    required: false
  nutanix_username:
    description:
      - PC username
    type: str
    required: true
  nutanix_password:
    description:
      - PC password;
    required: true
    type: str
  validate_certs:
    description:
      - Set value to C(False) to skip validation for self signed certificates
      - This is not recommended for production setup
    type: bool
    default: true
  state:
    description:
      - Specify state of INAME
      - If C(state) is set to C(present) then INAME is created.
      - >-
        If C(state) is set to C(absent) and if the INAME exists, then
        INAME is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for INAME CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: INAME Name
    required: False
    type: str
  INAME_uuid:
    description: INAME UUID
    type: str

  # Step 4: here should be additional arguments documentation

"""

EXAMPLES = r"""
# Step 5
"""

RETURN = r"""
# Step 6
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.MNAME import CNAME  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    module_args = dict(
    # Step 1: Ansible module spec and spec validation
    )

    return module_args


def create_INAME(module, result):
    INAME = CNAME(module)
    spec, error = INAME.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating INAME spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = INAME.create(spec)
    INAME_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["INAME_uuid"] = INAME_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = INAME.read(INAME_uuid)
        result["response"] = resp


def delete_INAME(module, result):
    INAME_uuid = module.params["INAME_uuid"]
    if not INAME_uuid:
        result["error"] = "Missing parameter INAME_uuid in playbook"
        module.fail_json(msg="Failed deleting INAME", **result)

    INAME = CNAME(module)
    resp = INAME.delete(INAME_uuid)
    result["changed"] = True
    result["response"] = resp
    result["INAME_uuid"] = INAME_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "INAME_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_INAME(module, result)
    elif state == "absent":
        delete_INAME(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

'''

client_sdk_content = """# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class CNAME(Prism):
    def __init__(self, module):
        resource_type = "/API_ENDPOINT"
        super(CNAME, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            # Step 2. This is a Map of
            # ansible attirbute and corresponding API spec generation method
            # Example: method name should start with _build_spec_<method_name>
            # name: _build_spec_name
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                # Step 3: Default API spec
            }
        )
"""


def create_module(args):
    """
    MNAME: Module name
    CNAME: Class name
    INAME: Function/Instance name
    API_ENDPOINT: URL prefix
    """

    api_endpoint = args.api.lower()
    name = api_endpoint[:-1]
    iname = args.iname if args.iname else name
    cname = args.cname if args.cname else name.capitalize()
    mname = args.mname if args.mname else api_endpoint

    success = True
    module = "plugins/modules/ntnx_{0}.py".format(mname)
    if os.path.exists(module):
        print("Aborting: {0} already exists".format(module))
        success = False
    else:
        with open(module, "w") as f:
            f.write(
                ansible_module_content.replace("MNAME", mname)
                .replace("CNAME", cname)
                .replace("INAME", iname)
            )
            print("Successfully generated code: {0}".format(module))

    sdk = "plugins/module_utils/prism/{0}.py".format(mname)
    if os.path.exists(sdk):
        print("Aborting: {0} already exists".format(sdk))
        success = False
        return success

    with open(sdk, "w") as f:
        f.write(
            client_sdk_content.replace("MNAME", mname)
            .replace("CNAME", cname)
            .replace("INAME", iname)
            .replace("API_ENDPOINT", api_endpoint)
        )
        print("Successfully generated code: {0}".format(sdk))
    return success


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("api", help="api endpoint")
    parser.add_argument("-m", "--mname", help="ansible module name")
    parser.add_argument("-c", "--cname", help="class name of the entity")
    parser.add_argument("-i", "--iname", help="instance name of the entity")
    args = parser.parse_args()

    if not create_module(args):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
