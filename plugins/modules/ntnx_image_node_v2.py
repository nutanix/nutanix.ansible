#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_node_v2
short_description: Image a node managed by Foundation Central
version_added: 2.7.0
description:
  - This module triggers an imaging operation on a node managed by Foundation Central.
  - Imaging installs the host OS (hypervisor) and/or AOS on the node using a patched image or installation details.
  - This is an action module and does not implement Create/Update/Delete state machines.
  - This module uses the Life Cycle Management v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central) (FCVM/Foundation), NOT to Prism Central.
    Set C(nutanix_host) to the Foundation Central endpoint.
  - >-
    B(Image a Node) - Requires the appropriate Foundation Central administrator role on the FCVM.
  - The node identified by C(ext_id) must exist and be in a state that allows imaging.
  - Exactly one of the C(configuration) suboptions must be provided.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will image the node.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID of the node to image.
    type: str
    required: true
  configuration:
    description:
      - The imaging configuration to apply to the node.
      - Exactly one of the suboptions must be provided.
    type: dict
    required: true
    suboptions:
      host_installation_details:
        description:
          - Details required to install the host OS (hypervisor) using a patched image.
        type: dict
        required: false
        suboptions:
          patched_image_ext_id:
            description:
              - External ID of the patched image to use for host installation.
            type: str
            required: false
          patched_image_url:
            description:
              - URL of the patched image to use for host installation.
            type: str
            required: false
      aos_installation_details:
        description:
          - Details required to install AOS on the node.
        type: dict
        required: false
        suboptions:
          name_servers:
            description:
              - List of DNS name server IP addresses/FQDNs to configure.
            type: list
            elements: str
            required: false
          ntp_servers:
            description:
              - List of NTP server IP addresses/FQDNs to configure.
            type: list
            elements: str
            required: false
          cvm_memory_gb:
            description:
              - Memory in GB to assign to the Controller VM.
            type: int
            required: false
          network_details:
            description:
              - Network configuration to apply during AOS installation.
            type: dict
            required: false
          aos_image_details:
            description:
              - Details of the AOS image to install.
            type: dict
            required: false
      hci_imaging_details:
        description:
          - Details required to perform hyperconverged (HCI) imaging of the node.
        type: dict
        required: false
        suboptions:
          hypervisor_details:
            description:
              - Hypervisor imaging details.
            type: dict
            required: false
          aos_details:
            description:
              - AOS imaging details.
            type: dict
            required: false
      reconfiguration_details:
        description:
          - Details required to reconfigure an already imaged node.
        type: dict
        required: false
        suboptions:
          host_details:
            description:
              - Host reconfiguration details.
            type: dict
            required: false
          cvm_details:
            description:
              - Controller VM reconfiguration details.
            type: dict
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
- name: Image a node using a patched host image
  nutanix.ncp.ntnx_image_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    configuration:
      host_installation_details:
        patched_image_ext_id: "b2b2b2b2-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true

- name: Image a node by installing AOS
  nutanix.ncp.ntnx_image_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    configuration:
      aos_installation_details:
        name_servers:
          - "10.0.0.10"
        ntp_servers:
          - "pool.ntp.org"
        cvm_memory_gb: 32
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for imaging a node.
    - Task details when C(wait) is true.
  returned: always
  type: dict
  sample:
    {
      "completed_time": "2026-09-09T06:26:51.524581+00:00",
      "created_time": "2026-09-09T06:26:47.167906+00:00",
      "entities_affected": [
        {"ext_id": "d1a1a1a1-1111-2222-3333-444455556666", "rel": "lifecycle:config:node"}
      ],
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "operation": "ImageNode",
      "operation_description": "Image node",
      "status": "SUCCEEDED"
    }

changed:
  description: This indicates whether the action was executed.
  returned: always
  type: bool
  sample: true

task_ext_id:
  description: The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the node.
  returned: when applicable
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

skipped:
  description: This indicates whether the action was skipped (e.g. in check mode).
  returned: when applicable
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Node with ext_id:d1a1a1a1-1111-2222-3333-444455556666 will be imaged."

error:
  description: This field holds the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_nodes_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    host_installation_details_spec = dict(
        patched_image_ext_id=dict(type="str", required=False),
        patched_image_url=dict(type="str", required=False),
    )

    aos_installation_details_spec = dict(
        name_servers=dict(type="list", elements="str", required=False),
        ntp_servers=dict(type="list", elements="str", required=False),
        cvm_memory_gb=dict(type="int", required=False),
        network_details=dict(type="dict", required=False),
        aos_image_details=dict(type="dict", required=False),
    )

    hci_imaging_details_spec = dict(
        hypervisor_details=dict(type="dict", required=False),
        aos_details=dict(type="dict", required=False),
    )

    reconfiguration_details_spec = dict(
        host_details=dict(type="dict", required=False),
        cvm_details=dict(type="dict", required=False),
    )

    configuration_spec = dict(
        host_installation_details=dict(
            type="dict",
            options=host_installation_details_spec,
            obj=lifecycle_sdk.HostInstallationDetails,
        ),
        aos_installation_details=dict(
            type="dict",
            options=aos_installation_details_spec,
            obj=lifecycle_sdk.AosInstallationDetails,
        ),
        hci_imaging_details=dict(
            type="dict",
            options=hci_imaging_details_spec,
            obj=lifecycle_sdk.HciImagingDetails,
        ),
        reconfiguration_details=dict(
            type="dict",
            options=reconfiguration_details_spec,
            obj=lifecycle_sdk.ReconfigurationDetails,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        configuration=dict(
            type="dict",
            required=True,
            options=configuration_spec,
            obj={
                "host_installation_details": lifecycle_sdk.HostInstallationDetails,
                "aos_installation_details": lifecycle_sdk.AosInstallationDetails,
                "hci_imaging_details": lifecycle_sdk.HciImagingDetails,
                "reconfiguration_details": lifecycle_sdk.ReconfigurationDetails,
            },
            mutually_exclusive=[
                (
                    "host_installation_details",
                    "aos_installation_details",
                    "hci_imaging_details",
                    "reconfiguration_details",
                )
            ],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ext_id", "configuration"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ImageNodeSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for imaging node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Node with ext_id:{0} will be imaged.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.image_node(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while imaging node with ext_id: {0}".format(
                ext_id
            ),
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_nodes_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
