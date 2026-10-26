#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_product_v2
short_description: Update the status of a portfolio Product in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module updates the status of a portfolio product in Nutanix Prism Central.
  - Use C(state=present) with C(ext_id) to update a product. Set
    C(enablement_state) to C(ENABLED) or C(DISABLED) to request the
    corresponding enable or disable workflow in Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Update a Product) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  state:
    description:
      - Specify state.
      - If C(state) is set to C(present), the module will update the product.
      - C(absent) is not supported because the Product API does not support delete.
    type: str
    choices:
      - present
    default: present
  domain_manager_ext_id:
    description:
      - The external identifier of the domain manager resource that
        owns the product.
      - Required for update operation.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the product.
      - Required for update operation.
    type: str
    required: true
  name:
    description:
      - Name of the product.
    type: str
    required: false
    choices:
      - FLOW_CONTROLLER
      - FLOW_NETWORK_SECURITY
      - FLOW_VIRTUAL_NETWORKING
      - INTELLIGENT_OPERATIONS
      - NUTANIX_CLOUD_MANAGER
      - NUTANIX_DISASTER_RECOVERY
      - NUTANIX_MARKETPLACE
      - SELF_SERVICE
  enablement_state:
    description:
      - Enablement state of the product.
      - Required for update operation.
      - Set to C(ENABLED) to enable and C(DISABLED) to disable the product.
      - Some products cannot be disabled once they have been enabled.
    type: str
    required: false
    choices:
      - ENABLED
      - DISABLED
  metadata:
    description:
      - Metadata associated with the given product. This field is a no-op for
        products that do not require additional user inputs.
      - Only one of the two suboption groups may be provided.
    type: dict
    required: false
    suboptions:
      generic_metadata:
        description:
          - Generic key-value attributes to associate with the product.
        type: dict
        required: false
        suboptions:
          attributes:
            description:
              - List of key-value pairs describing the product metadata.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Attribute name.
                type: str
                required: false
              value:
                description:
                  - The value associated with the key for this key-value pair.
                  - Can be a string, integer, boolean, object, or a list of
                    strings/integers/objects as defined by the API.
                type: raw
                required: false
      flow_controller_metadata:
        description:
          - Additional user inputs required to enable the Flow Controller product.
        type: dict
        required: false
        suboptions:
          cloud_substrate:
            description:
              - Cloud substrate on which the Flow Controller is deployed.
            type: str
            required: false
            choices:
              - AWS
              - AZURE
              - GCP
          cluster_ext_id:
            description:
              - External identifier of the cluster on which the Flow Controller is
                deployed.
            type: str
            required: false
          subnet_ext_id:
            description:
              - External identifier of the subnet on which the Flow Controller is
                deployed.
            type: str
            required: false
          is_fns_flex_mode_enabled:
            description:
              - Indicates whether the Flow Controller should operate in Flex mode
                or App-centric mode for Flow Network Security policies.
              - Flex mode uses standard 5-tuple network definitions (source,
                destination, protocol, ports) for more explicit control.
              - App-centric mode uses the traditional secured entity-based approach.
            type: bool
            required: false
            default: false
          size:
            description:
              - Size of the Flow Controller deployment.
            type: str
            required: false
            choices:
              - SMALL
              - LARGE
              - XLARGE
          is_security_analytics_enabled:
            description:
              - Indicates whether the Security Analytics feature is enabled for
                the Flow Controller.
            type: bool
            required: false
            default: true
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
- name: Enable a portfolio product
  nutanix.ncp.ntnx_product_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    ext_id: "d62e6046-e7b0-4848-6909-fe5cfe476d51"
    enablement_state: "ENABLED"
  register: enable_result
  ignore_errors: true

- name: Disable a portfolio product
  nutanix.ncp.ntnx_product_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    ext_id: "d62e6046-e7b0-4848-6909-fe5cfe476d51"
    enablement_state: "DISABLED"
  register: disable_result
  ignore_errors: true

- name: Update Flow Controller product metadata
  nutanix.ncp.ntnx_product_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    ext_id: "1b865ccc-02bb-4dc4-4933-8e576b54a9a9"
    name: "FLOW_CONTROLLER"
    enablement_state: "ENABLED"
    metadata:
      flow_controller_metadata:
        cloud_substrate: "AWS"
        cluster_ext_id: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
        subnet_ext_id: "9306c8d3-bb00-4b98-b354-ef2dfbd2c7ba"
  register: fc_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the portfolio product.
    - If C(wait) is true, it will contain the final product details as
      returned by C(get_product_by_id) after the enablement task completes.
    - If C(wait) is false, it will contain the task details returned by the
      update operation.
  returned: always
  type: dict
  sample:
    {
      "enablement_state": "ENABLED",
      "ext_id": "0081eaf6-527b-44a0-4fe9-60ee067c0e82",
      "last_modified_time": "2026-06-30T17:30:02.650540+00:00",
      "links": null,
      "metadata": null,
      "name": "SELF_SERVICE",
      "resize_time": "2026-06-30T17:11:25.349000+00:00",
      "resource_spec": {
        "cpu_count": 2,
        "memory_size_bytes": 4294967296
      },
      "service_enablement_time": null,
      "tenant_id": null,
      "version": null
    }

task_ext_id:
  description:
    - The external ID of the task triggered by the update operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the portfolio product.
  returned: always
  type: str
  sample: "0081eaf6-527b-44a0-4fe9-60ee067c0e82"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating update product spec"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import get_product  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Server populated attributes that must NOT be sent back in the update body.
_PRODUCT_READ_ONLY_FIELDS = (
    "service_enablement_time",
    "resize_time",
    "last_modified_time",
    "version",
    "links",
    "tenant_id",
)


def get_module_spec():

    resource_spec = dict(
        cpu_count=dict(type="int", required=False),
        memory_size_bytes=dict(type="int", required=False),
    )

    generic_metadata_attribute_spec = dict(
        name=dict(type="str", required=False),
        value=dict(type="raw", required=False),
    )

    generic_metadata_spec = dict(
        attributes=dict(
            type="list",
            elements="dict",
            options=generic_metadata_attribute_spec,
            required=False,
            obj=prism_sdk.KVPair,
        ),
    )

    flow_controller_metadata_spec = dict(
        cloud_substrate=dict(
            type="str",
            required=False,
            choices=["AWS", "AZURE", "GCP"],
            obj=prism_sdk.CloudSubstrateType,
        ),
        cluster_ext_id=dict(type="str", required=False),
        subnet_ext_id=dict(type="str", required=False),
        is_fns_flex_mode_enabled=dict(type="bool", required=False, default=False),
        size=dict(
            type="str",
            required=False,
            choices=["SMALL", "LARGE", "XLARGE"],
            obj=prism_sdk.FlowControllerSize,
        ),
        is_security_analytics_enabled=dict(
            type="bool", required=False, default=True
        ),
    )

    metadata_spec = dict(
        generic_metadata=dict(
            type="dict",
            options=generic_metadata_spec,
            required=False,
            obj=prism_sdk.GenericMetadata,
        ),
        flow_controller_metadata=dict(
            type="dict",
            options=flow_controller_metadata_spec,
            required=False,
            obj=prism_sdk.FlowControllerMetadata,
        ),
    )

    metadata_allowed_types = {
        "generic_metadata": prism_sdk.GenericMetadata,
        "flow_controller_metadata": prism_sdk.FlowControllerMetadata,
    }

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        domain_manager_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        name=dict(
            type="str",
            required=False,
            choices=[
                "FLOW_CONTROLLER",
                "FLOW_NETWORK_SECURITY",
                "FLOW_VIRTUAL_NETWORKING",
                "INTELLIGENT_OPERATIONS",
                "NUTANIX_CLOUD_MANAGER",
                "NUTANIX_DISASTER_RECOVERY",
                "NUTANIX_MARKETPLACE",
                "SELF_SERVICE",
            ],
            obj=prism_sdk.ProductName,
        ),
        version=dict(type="str", required=False),
        enablement_state=dict(
            type="str",
            required=False,
            choices=["ENABLED", "DISABLED"],
            obj=prism_sdk.EnablementState,
        ),
        resource_spec=dict(
            type="dict",
            options=resource_spec,
            required=False,
            obj=prism_sdk.ManagementResourceSpec,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            required=False,
            obj=metadata_allowed_types,
            mutually_exclusive=[("generic_metadata", "flow_controller_metadata")],
        ),
    )
    return module_args


def update_Product(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["enablement_state"])

    current_spec = get_product(module, api_instance, ext_id, domain_manager_ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating product with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update product spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    strip_read_only_fields(update_spec, fields=_PRODUCT_READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_product_by_id(
            domainManagerExtId=domain_manager_ext_id,
            extId=ext_id,
            body=update_spec,
            if_match=etag,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating product with ext_id: {0}".format(
                ext_id
            ),
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_product(module, api_instance, ext_id, domain_manager_ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_domain_manager_api_instance(module)
    update_Product(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
