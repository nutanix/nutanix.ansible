#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vcenter_integration_v2
short_description: Register or unregister vCenter server integration in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to register (C(state=present)) or unregister
    (C(state=absent)) a vCenter server integration for a cluster registered to
    Nutanix Prism Central.
  - The vCenter server integration objects are discovered by Prism Central for
    every cluster it manages. An C(ext_id) that identifies the integration must
    be supplied for every register / unregister call; you can obtain the
    C(ext_id) using M(nutanix.ncp.ntnx_vcenter_integrations_info_v2).
  - Update is not supported by the vCenter server integration API.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Register vCenter integration) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Unregister vCenter integration) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present), the vCenter server integration identified
        by C(ext_id) will be registered using the supplied credentials.
      - If C(state) is set to C(absent), the vCenter server integration identified
        by C(ext_id) will be unregistered.
      - Update is not supported by the vCenter server integration API.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The globally unique identifier of the vCenter server integration instance
        (UUID). It should match the C(ext_id) returned by the
        M(nutanix.ncp.ntnx_vcenter_integrations_info_v2) list operation.
    type: str
    required: true
  username:
    description:
      - Username used to authenticate the vCenter server integration during
        registration.
      - Required for registration.
    type: str
    required: false
  password:
    description:
      - Password used to authenticate the vCenter server integration during
        registration.
      - Required for registration.
    type: str
    required: false
  port:
    description:
      - Port number used to connect to the vCenter server when registering the
        integration. Defaults to 443.
    type: int
    required: false
    default: 443
  authentication_method:
    description:
      - Authentication method used for the vCenter server integration, such as SSO
        or EXTENSION.
    type: str
    required: false
    choices:
      - SSO
      - EXTENSION
  config:
    description:
      - Unregister payload. EXTENSION requires username and password. SSO does not
        require credentials.
      - Provide exactly one of the oneOf variants.
    type: dict
    required: false
    suboptions:
      extension_config:
        description:
          - Unregister an EXTENSION integration. Username and password are required.
        type: dict
        required: false
        suboptions:
          username:
            description:
              - Username used to authenticate the vCenter server integration during
                unregistration.
            type: str
            required: true
          password:
            description:
              - Password used to authenticate the vCenter server integration during
                unregistration.
            type: str
            required: true
      sso_config:
        description:
          - Unregister an SSO integration. No credentials are required.
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
- name: Register vCenter server integration
  nutanix.ncp.ntnx_vcenter_integration_v2:
    state: present
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
    username: "administrator@vsphere.local"
    password: "vcenter-admin-password"
    port: 443
    authentication_method: "EXTENSION"
  register: register_result

- name: Unregister vCenter server integration with EXTENSION
  nutanix.ncp.ntnx_vcenter_integration_v2:
    state: absent
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
    config:
      extension_config:
        username: "administrator@vsphere.local"
        password: "vcenter-admin-password"
  register: unregister_result

- name: Unregister vCenter server integration with SSO
  nutanix.ncp.ntnx_vcenter_integration_v2:
    state: absent
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
    config:
      sso_config: {}
  register: unregister_sso_result
"""

RETURN = r"""
response:
  description:
    - Response for registering or unregistering a vCenter server integration.
    - If the operation is register and C(wait) is true, it will return the
      refreshed vCenter server integration details.
    - If the operation is register and C(wait) is false, it will return the
      task details.
    - If the operation is unregister, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "authentication_method": "EXTENSION",
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "connection_status": "CONNECTED",
      "ext_id": "00061c8b-2f6e-4a1c-8b41-abc123abc123",
      "ip_address": "10.10.10.20",
      "is_registered": true,
      "links": null,
      "port": 443,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the vCenter server integration.
  returned: always
  type: str
  sample: "00061c8b-2f6e-4a1c-8b41-abc123abc123"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "vCenter integration with ext_id '00061c8b-2f6e-4a1c-8b41-abc123abc123' is already registered. Skipping registration."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_vcenter_integrations_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_vcenter_integration,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    extension_unregister_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    sso_unregister_spec = dict()

    config_spec = dict(
        extension_config=dict(
            type="dict",
            options=extension_unregister_spec,
            obj=cluster_management_sdk.VcenterExtensionUnregisterParams,
            required=False,
        ),
        sso_config=dict(
            type="dict",
            options=sso_unregister_spec,
            obj=cluster_management_sdk.VcenterSsoUnregisterParams,
            required=False,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        port=dict(type="int", required=False, default=443),
        authentication_method=dict(
            type="str",
            required=False,
            choices=["SSO", "EXTENSION"],
            obj=cluster_management_sdk.VcenterIntegrationAuthenticationMethod,
        ),
        config=dict(
            type="dict",
            options=config_spec,
            obj={
                "extension_config": cluster_management_sdk.VcenterExtensionUnregisterParams,  # noqa: E501
                "sso_config": cluster_management_sdk.VcenterSsoUnregisterParams,  # noqa: E501
            },
            required=False,
        ),
    )
    return module_args


def create_vcenter_integration(module, result, api_instance):
    """Register a vCenter server integration."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    # Validate required params for register before fetching current
    for field in ["username", "password", "authentication_method"]:
        if not module.params.get(field):
            module.fail_json(
                msg="missing required arguments: {0}".format(field), **result
            )

    current = get_vcenter_integration(module, api_instance, ext_id)
    etag = get_etag(data=current)

    if getattr(current, "is_registered", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        module.exit_json(
            msg=(
                "vCenter integration with ext_id '{0}' is already registered. "
                "Skipping registration."
            ).format(ext_id),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.VcenterIntegrationRegisterParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating register vCenter integration spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = {"if_match": etag} if etag else {}
    try:
        resp = api_instance.register_vcenter_integration(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while registering vCenter integration",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_vcenter_integration(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def delete_vcenter_integration(module, result, api_instance):
    """Unregister a vCenter server integration."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = get_vcenter_integration(module, api_instance, ext_id)
    etag = get_etag(data=current)

    if not getattr(current, "is_registered", True):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        module.exit_json(
            msg=(
                "vCenter integration with ext_id '{0}' is already unregistered. "
                "Skipping unregistration."
            ).format(ext_id),
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "vCenter integration with ext_id:{0} will be unregistered.".format(ext_id)
        )
        return

    # Build unregister spec
    sg = SpecGenerator(module)
    # If config is provided, use it; otherwise default to SSO (empty)
    if module.params.get("config"):
        default_spec = cluster_management_sdk.VcenterIntegrationUnregisterParams()
        spec, err = sg.generate_spec(obj=default_spec)
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed generating unregister vCenter integration spec", **result
            )
    else:
        # Default to SSO when no config supplied
        default_spec = cluster_management_sdk.VcenterIntegrationUnregisterParams(
            config=cluster_management_sdk.VcenterSsoUnregisterParams()
        )
        spec = default_spec

    kwargs = {"if_match": etag} if etag else {}
    try:
        resp = api_instance.unregister_vcenter_integration(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unregistering vCenter integration",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vcenter_integrations_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_vcenter_integration(module, result, api_instance)
    else:
        delete_vcenter_integration(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
