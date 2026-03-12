#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_user_v2
short_description: Manage snmp users in Nutanix Prism Central
version_added: 2.6.0
description:
  - Create, Update, Delete snmp users.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - If C(state) is present, it will create or update the snmp user.
      - If C(state) is set to C(present) and ext_id is not provided, the operation will create the snmp user.
      - If C(state) is set to C(present) and ext_id is provided, the operation will update the snmp user.
      - If C(state) is set to C(absent) and ext_id is provided, the operation will delete the snmp user.
    type: str
    choices: ['present', 'absent']
  ext_id:
    description:
      - SnmpUser external ID.
      - Required for updating or deleting the snmp user.
    type: str
  cluster_ext_id:
    description:
      - The external ID of the parent cluster.
    type: str
    required: true
  username:
    description:
      - SNMP username. For SNMP trap v3 version, SNMP username is required parameter.
    type: str
    required: true
  auth_type:
    description:
      - Auth type.
    type: str
    required: true
    choices: ['MD5', 'SHA']
  auth_key:
    description:
      - SNMP user authentication key.
    type: str
    required: true
  priv_type:
    description:
      - Priv type.
    type: str
    choices: ['DES', 'AES']
  priv_key:
    description:
      - SNMP user encryption key.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create snmp user
  nutanix.ncp.ntnx_snmp_user_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    username: "my_snmp_user"
    auth_type: SHA
    auth_key: "my_auth_key_123"
  register: result

- name: Update snmp user
  nutanix.ncp.ntnx_snmp_user_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    ext_id: "{{ snmp_user_ext_id }}"
    username: "my_snmp_user"
    auth_type: MD5
    auth_key: "updated_auth_key_123"
  register: result

- name: Delete snmp user
  nutanix.ncp.ntnx_snmp_user_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    ext_id: "{{ snmp_user_ext_id }}"
  register: result
"""

RETURN = r"""
response:
  description:
  - The response for snmp user operations.
  - SNMP config details if operation is create and C(wait) is True.
  - SNMP user details if operation is update and C(wait) is True.
  - Task details if operation is delete and C(wait) is True.
  type: dict
  returned: always
  sample:
    {
      "auth_key": null,
      "auth_type": "SHA",
      "ext_id": "84a60289-e6b6-4814-b882-7858f5485a24",
      "links": null,
      "priv_key": null,
      "priv_type": "AES",
      "tenant_id": null,
      "username": "snmp_user_all_ansible_test_EriQKlYVhfgw"
    }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

error:
  description: Error message if something goes wrong.
  returned: always
  type: str
  sample: null

cluster_ext_id:
  description: The external ID of the cluster.
  returned: always
  type: str
  sample: "913fa076-d385-4dd8-b549-0e628e645569"

ext_id:
  description: The external ID of the snmp user that was updated or deleted.
  returned: always
  type: str
  sample: "84a60289-e6b6-4814-b882-7858f5485a24"

task_ext_id:
  description: Task External ID
  returned: always
  type: str
  sample: "ZXJnb24=:54a506dc-6d4f-4344-43e4-41205eba32f4"

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating snmp user"

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_snmp_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_snmp_config,
    get_snmp_user,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
        username=dict(type="str"),
        auth_type=dict(
            type="str", choices=["MD5", "SHA"], obj=clusters_sdk.SnmpAuthType
        ),
        auth_key=dict(type="str", no_log=True),
        priv_type=dict(
            type="str", choices=["DES", "AES"], obj=clusters_sdk.SnmpPrivType
        ),
        priv_key=dict(type="str", no_log=True),
    )

    return module_args


def create_snmp_user(module, result, snmp_users, snmp_config_api):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.SnmpUser()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create snmp user spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = snmp_users.create_snmp_user(body=spec, clusterExtId=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating snmp user",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_snmp_config(module, snmp_config_api, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_snmp_user_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec.to_dict())
    update_spec = strip_internal_attributes(update_spec.to_dict())
    old_spec.pop("auth_key")
    update_spec.pop("auth_key")
    old_spec.pop("priv_key")
    update_spec.pop("priv_key")
    if old_spec != update_spec:
        return False
    return True


def update_snmp_user(module, result, snmp_users, snmp_config_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    current_spec = get_snmp_user(
        module, snmp_users, ext_id=ext_id, cluster_ext_id=cluster_ext_id
    )
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating snmp user", **result)

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snmp user update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    result["current_spec"] = strip_internal_attributes(current_spec.to_dict())
    result["update_spec"] = strip_internal_attributes(update_spec.to_dict())

    if check_snmp_user_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = snmp_users.update_snmp_user_by_id(
            extId=ext_id, body=update_spec, clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating snmp user",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_snmp_user(
            module, snmp_users, ext_id=ext_id, cluster_ext_id=cluster_ext_id
        )
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_snmp_user(module, result, snmp_users, snmp_config_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    if module.check_mode:
        result["msg"] = "SnmpUser with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = snmp_users.delete_snmp_user_by_id(
            extId=ext_id, clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting snmp user",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("username", "auth_type", "auth_key")),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "cluster_ext_id": None,
    }
    api_instance = get_snmp_api_instance(module)
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_snmp_user(module, result, api_instance, api_instance)
        else:
            create_snmp_user(module, result, api_instance, api_instance)
    else:
        delete_snmp_user(module, result, api_instance, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
