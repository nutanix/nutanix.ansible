#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_config_info_v2
short_description: Get PC Configuration info
version_added: 2.1.0
description:
    - Fetch specific PC Configuration info using external ID
    - Fetch list of multiple PC Configuration info if external ID is not provided with optional filters
options:
    ext_id:
        description: External ID to fetch specific PC Configuration info
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all PCs
  nutanix.ncp.ntnx_pc_config_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: Fetch PC details using external ID
  nutanix.ncp.ntnx_pc_config_info_v2:
    ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result

- name: List all PCs with filter
  nutanix.ncp.ntnx_pc_config_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: extId eq '{{ domain_manager_ext_id }}'
  register: pc_details
"""

RETURN = r"""
response:
    description:
        - Response for fetching PC Configuration info
        - PC Configuration info if external ID is provided
        - List of multiple PC Configuration info if external ID is not provided
    type: dict
    returned: always
    sample:
    {}

ext_id:
    description: External ID of the PC
    type: str
    returned: always
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_pc_config_with_ext_id(module, domain_manager_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_pc_config(module, domain_manager_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_pc_configs(module, domain_manager_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PC Configuration info Spec", **result)
    try:
        resp = domain_manager_api.list_domain_managers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching PC Configuration info",
        )
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    domain_manager_api = get_domain_manager_api_instance(module)
    if module.params.get("ext_id"):
        get_pc_config_with_ext_id(module, domain_manager_api, result)
    else:
        get_pc_configs(module, domain_manager_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
