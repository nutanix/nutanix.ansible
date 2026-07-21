#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_descriptors_v4_v2
short_description: Placeholder CRUD module for aiops EntityDescriptorsV4 (read-only entity)
version_added: 2.7.0
description:
  - The aiops V(EntityDescriptorsV4) resource is a read-only catalog of entity
    types and their metric/attribute descriptors. The underlying SDK
    (V(ntnx_aiops_py_client)) exposes only a list operation
    (V(GET /api/aiops/v4.2.b1/config/sources/{sourceExtId}/entity-descriptors))
    and no create/update/delete APIs.
  - This module is generated for interface parity with other v2 modules but
    will fail with a descriptive message on any C(state) invocation because
    no CRUD operation is supported by the API.
  - Use M(nutanix.ncp.ntnx_entity_descriptors_info_v2) instead to fetch
    entity descriptors.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module will always fail. It exists only so that the generated
      module surface mirrors the CRUD/info pair used by other v2 modules.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - Ignored. Present for interface parity; any value will result in a
        descriptive failure.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - Ignored. Present for interface parity.
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
- name: Any invocation fails — EntityDescriptorsV4 has no CRUD API
  nutanix.ncp.ntnx_entity_descriptors_v4_v2:
    state: present
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: Always null — no CRUD operation is available for this entity.
  returned: always
  type: dict
  sample: null

task_ext_id:
  description: Always null — no task is created because no CRUD operation is available.
  returned: always
  type: str
  sample: null

ext_id:
  description: Echo of the C(ext_id) input if any.
  returned: always
  type: str
  sample: null

changed:
  description: Always false — nothing can be changed for a read-only entity.
  returned: always
  type: bool
  sample: false

skipped:
  description: Always true when the module short-circuits because no CRUD API is available.
  returned: always
  type: bool
  sample: true

error:
  description: Error details when the module refuses to run.
  returned: When an error occurs
  type: str
  sample: "EntityDescriptorsV4 has no CRUD API; use ntnx_entity_descriptors_info_v2"

failed:
  description: Always true — every invocation is rejected.
  returned: always
  type: bool
  sample: true

msg:
  description: Human readable explanation of why the module refused to run.
  returned: always
  type: str
  sample: "EntityDescriptorsV4 is a read-only aiops resource. Use ntnx_entity_descriptors_info_v2 to list entity/metric descriptors."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_NO_CRUD_MSG = (
    "EntityDescriptorsV4 is a read-only aiops resource. "
    "The ntnx_aiops_py_client SDK only exposes a list operation "
    "(get_entity_descriptors_v4). "
    "Use ntnx_entity_descriptors_info_v2 to list entity/metric descriptors."
)


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "failed": True,
        "skipped": True,
        "ext_id": module.params.get("ext_id"),
        "task_ext_id": None,
        "error": _NO_CRUD_MSG,
        "msg": _NO_CRUD_MSG,
    }
    module.fail_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
