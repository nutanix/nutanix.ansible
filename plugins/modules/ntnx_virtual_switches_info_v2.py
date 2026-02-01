#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_switches_info_v2
short_description: Fetch virtual switches info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch virtual switches info or specific virtual switch in Nutanix Prism Central.
  - If ext_id is provided, fetch particular virtual switch info using external ID
  - If ext_id is not provided, fetch multiple virtual switches info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external identifier of the virtual switch.
    type: str
  cluster_ext_id:
    description:
      - Prism Element cluster UUID to be passed in X-Cluster-Id header.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
"""
RETURN = r"""
response:
  description:
    - Response for fetching virtual switches info
    - Specific virtual switch info if External ID is provided
    - List of multiple virtual switches info if External ID is not provided
  returned: always
  type: dict

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching virtual switches info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs
  sample: null

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the virtual switch
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available virtual switches in PC.
  type: int
  returned: when all virtual switches are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_virtual_switches_api_instance,
)
from ..module_utils.v4.network.helpers import get_virtual_switch  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def get_virtual_switch_using_ext_id(module, virtual_switches, result):
    ext_id = module.params.get("ext_id")
    kwargs = {}
    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")
    resp = get_virtual_switch(module, virtual_switches, ext_id, **kwargs)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virtual_switches(module, virtual_switches, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating virtual switches info Spec", **result)

    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    try:
        resp = virtual_switches.list_virtual_switches(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual switches info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "error": None}
    virtual_switches = get_virtual_switches_api_instance(module)
    if module.params.get("ext_id"):
        get_virtual_switch_using_ext_id(module, virtual_switches, result)
    else:
        get_virtual_switches(module, virtual_switches, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
