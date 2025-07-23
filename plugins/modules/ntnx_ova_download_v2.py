#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ova_download_v2
short_description: "Download an OVA file"
version_added: 2.3.0
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""

"""
RETURN = r"""

"""


import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import ( # noqa: E402
    get_ova_api_instance,
)

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
        ova_ext_id=dict(type="str", required=True),
    )
    return module_args


def download_ova(module, result):
    ova_ext_id = module.params.get("ova_ext_id")
    result["ext_id"] = ova_ext_id
    ova = get_ova_api_instance(module)

    if module.check_mode:
        result["msg"] = "Ova with ext_id:{0} will be downloaded.".format(ova_ext_id)
        return

    resp = None
    try:
        resp = ova.get_file_by_ova_id(
            ovaExtId=ova_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading ova",
        )
    path = resp.to_dict().get("data").get("path")
    result["response"] = {
        "path": path,
    }
    result["changed"] = True


def run_module():
    module = BaseInfoModule(
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
    download_ova(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
