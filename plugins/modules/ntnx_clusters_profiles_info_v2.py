#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_profiles_info_v2
short_description: Retrieve information about Nutanix cluster profiles from PC
version_added: 2.4.0
description:
    - This module retrieves information about Nutanix cluster profiles from PC.
    - Fetch particular cluster profile info using external ID
    - Fetch multiple clusters info with/without using filters, limit, etc.
    - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the cluster profile.
      - If not provided, multiple cluster profiles info will be fetched.
    type: str
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: fetch cluster profile info using external ID
  nutanix.ncp.ntnx_clusters_profiles_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
  register: result

- name: fetch all cluster profiles info
  nutanix.ncp.ntnx_clusters_profiles_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: fetch all clusters info with filter
  nutanix.ncp.ntnx_clusters_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "name eq 'cluster_profile_1'"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching cluster profile info.
        - Returns cluster profile info if ext_id is provided or list of multiple cluster profiles.
    type: dict
    returned: always
    sample:
changed:
    description:
        - Indicates if any changes were made during the operation.
    type: bool
    returned: always
    sample: true
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
ext_id:
    description:
        - The external ID of the cluster profile if given in input.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_profiles_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_profile  # noqa: E402
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
    )

    return module_args


def get_cluster_profile_by_ext_id(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    resp = get_cluster_profile(module, cluster_profiles, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_profiles(module, cluster_profiles, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json(
            "Failed creating query parameters for fetching cluster profiles info"
        )
    resp = None
    try:
        resp = cluster_profiles.list_cluster_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster profiles info",
        )

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    cluster_profiles = get_cluster_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_cluster_profile_by_ext_id(module, cluster_profiles, result)
    else:
        get_cluster_profiles(module, cluster_profiles, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
