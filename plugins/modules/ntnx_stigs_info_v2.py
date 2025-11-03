#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_stigs_info_v2
short_description: Fetch Security Technical Implementation Guide (STIG) rule details and issue counts for each cluster
version_added: 2.4.0
description:
  - A Security Technical Implementation Guide (STIG) is a cybersecurity methodology for standardizing security protocols within networks, servers, computers,
    and logical designs to enhance overall security.
  - These guides, when implemented, enhance security for software, hardware, and physical and logical architectures to further reduce vulnerabilities.
  - This module retrieves Security Technical Implementation Guide (STIG) control details for each cluster.
  - Each STIG record represents a specific rule or control evaluated against one or more clusters, containing metadata such as rule ID, severity, compliance status,
    and remediation guidance.
  - This module uses PC v4 APIs based SDKs.
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch detailed Security Technical Implementation Guide control information for each cluster.
  nutanix.ncp.ntnx_stigs_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: Fetch detailed Security Technical Implementation Guide control information for each cluster with filter
  nutanix.ncp.ntnx_stigs_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "severity eq Security.Report.Severity'LOW'"
  register: result_filter

- name: Fetch detailed Security Technical Implementation Guide control information for each cluster with limit
  nutanix.ncp.ntnx_stigs_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    limit: 1
  register: result_limit
"""

RETURN = r"""
response:
  description:
    - Response for fetching Security Technical Implementation Guide details.
    - A list of Security Technical Implementation Guide control details for each cluster.
  type: dict
  returned: always
  sample:
    [
      {
        "affected_clusters": ["00063e6e-18f3-aefb-0ace-e59ff1cc2885"],
        "benchmark_id": "RHEL_8_V2R2",docuemntation
        "comments": null,
        "ext_id": "15c1f2d3-4849-4929-50ba-5c7da6a748ba",
        "fix_text": "Configure RHEL 8 to enable kernel page-table isolation with the following command:\n\n
          $ sudo grubby --update-kernel=ALL --args=\"pti=on\"\n\n
          Add or modify the following line in \"/etc/default/grub\"
          to ensure the configuration survives kernel updates:\n\n
          GRUB_CMDLINE_LINUX=\"pti=on\"",
        "identifiers": null,
        "links": null,
        "rule_id": "SV-230491r1017274_rule",
        "severity": "LOW",
        "status": "APPLICABLE",
        "stig_version": "RHEL-08-040004",
        "tenant_id": null,
        "title": "RHEL 8 must enable mitigations against processor-based vulnerabilities.",
      },
      {
        "affected_clusters": ["00063e6e-18f3-aefb-0ace-e59ff1cc2885"],
        "benchmark_id": "RHEL_8_V2R2",
        "comments": null,
        "ext_id": "4a4863a1-93b3-4cc9-6f88-bdd0c8eec7dc",
        "fix_text": "Set the mode of the local initialization files to \"0740\" with the following command:\n\n
          Note: The example will be for the smithj user, who has a home directory of \"/home/smithj\".\n\n
          $ sudo chmod 0740 /home/smithj/.<INIT_FILE>",
        "identifiers": null,
        "links": null,
        "rule_id": "SV-230325r1017136_rule",
        "severity": "MEDIUM",
        "status": "APPLICABLE",
        "stig_version": "RHEL-08-010770",
        "tenant_id": null,
        "title": "All RHEL 8 local initialization files must have mode 0740 or less permissive.",
      },
    ]
changed:
  description: Indicates if any changes were made by the module.
  type: bool
  returned: always
  sample: false
failed:
  description: Indicates if the module execution failed.
  type: bool
  returned: always
  sample: false
error:
  description: Error message if any.
  type: str
  returned: always
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import get_stigs_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (
    raise_api_exception,
    strip_internal_attributes,
)  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def run_module():
    module = BaseInfoModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "error": None, "response": None}
    stig_api_instance = get_stigs_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Security Technical Implementation Guide info Spec",
            **result,
        )
    resp = None
    try:
        resp = stig_api_instance.list_stigs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Security Technical Implementation Guide control details",
        )
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
