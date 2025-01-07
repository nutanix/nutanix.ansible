#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_restore_source_info_v2
short_description: Get PC restore source info
version_added: 2.1.0
description:
    - Fetch specific restore source info using external ID
options:
    ext_id:
        description: External ID to fetch specific restore source info
        type: str
        required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.pe.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.prism.helpers import get_restore_source  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(ext_id=dict(type="str", required=True))
    return module_args


def get_restore_source_with_ext_id(module, prism, result):
    ext_id = module.params.get("ext_id")
    resp = get_restore_source(module, prism, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


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
    prism = get_domain_manager_backup_api_instance(module)
    if module.params.get("ext_id"):
        get_restore_source_with_ext_id(module, prism, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
