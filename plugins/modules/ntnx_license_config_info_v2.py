#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_license_config_info_v2
short_description: Lists license configurations
description:
    - Lists license configurations.
    - Shows the current state of the license.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.4.0"
author:
  - Abhinav Bansal (@abhinavbansal29)
options:
  page:
    description:
      - The number of page
    type: int
  limit:
    description:
      - The number of records
    type: int
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
"""

EXAMPLES = r"""
- name: Get license config info
  nutanix.ncp.ntnx_license_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: Get license config info using limit
  nutanix.ncp.ntnx_license_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix List license configurations API.
  type: dict
  returned: always
  sample:
    [
        {
            "enforcement_policy": "ALL",
            "ext_id": "00063e5a-2715-c792-0000-000000028f57",
            "has_non_compliant_features": false,
            "has_ultimate_trial_ended": false,
            "is_license_check_disabled": false,
            "is_multicluster": false,
            "is_standby": false,
            "license_class": "APPLIANCE",
            "license_key": null,
            "links": null,
            "logical_version": {
                "cluster_version": 0,
                "license_version": 0
            },
            "post_paid_config": {
                "billing_plan": "$UNKNOWN",
                "category": "$UNKNOWN",
                "consumption_type": "$UNKNOWN",
                "id": null,
                "is_pulse_required": false
            },
            "tenant_id": null
        }
    ]
changed:
    description:
        - Indicates whether the module has made any changes.
    type: bool
    returned: always
    sample: false
total_available_results:
    description:
        - The total number of available license configurations.
    type: int
    returned: when all license configurations are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.licensing.api_client import (  # noqa: E402
    get_licensing_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        page=dict(type="int"),
        limit=dict(type="int"),
    )
    return module_args


def license_config_info(module, licensing_api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating license config info Spec", **result)

    try:
        resp = licensing_api_instance.list_settings(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching license config info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }

    licensing_api_instance = get_licensing_api_instance(module)

    license_config_info(module, licensing_api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
