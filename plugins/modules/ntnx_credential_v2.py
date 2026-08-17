#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_credential_v2
short_description: Create, Update, Delete credentials in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete credentials in the Nutanix Prism Central credential store.
  - Credentials are used by day-2 operations (for example Life Cycle Manager inventory and upgrades) to authenticate with
    external management endpoints such as Baseboard Management Controllers (BMC), VMware vCenter servers, and
    Cisco Intersight.
  - Only one of C(credential_details.bmc), C(credential_details.vcenter) or C(credential_details.intersight) may be
    supplied for a given credential.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Credential) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update a Credential) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete a Credential) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a credential.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the credential.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the credential.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID of the credential.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the credential.
      - Required for create operation.
      - Minimum length is 1 character and maximum length is 256 characters.
    type: str
    required: false
  credential_details:
    description:
      - Details of the credential authentication parameters.
      - Exactly one of C(bmc), C(vcenter) or C(intersight) must be provided to select the credential type.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      bmc:
        description:
          - BMC (Baseboard Management Controller) credential using basic authentication.
        type: dict
        required: false
        suboptions:
          type:
            description:
              - Pre-defined type of credential.
            type: str
            required: false
          credential:
            description:
              - Basic authentication credential (username / password) for the BMC.
            type: dict
            required: false
            suboptions:
              username:
                description:
                  - Username required for the basic auth scheme.
                  - Minimum length is 3 characters and maximum length is 256 characters.
                type: str
                required: true
              password:
                description:
                  - Password required for the basic auth scheme.
                type: str
                required: true
      vcenter:
        description:
          - VMware vCenter credential using basic authentication.
        type: dict
        required: false
        suboptions:
          address:
            description:
              - Network address of the vCenter server (IPv4, IPv6 or FQDN).
              - Exactly one of C(ipv4), C(ipv6) or C(fqdn) should be supplied.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification for the vCenter server.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the network (0-32).
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification for the vCenter server.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the network (0-128).
                    type: int
                    required: false
              fqdn:
                description:
                  - Fully qualified domain name of the vCenter server.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The FQDN value.
                    type: str
                    required: true
          type:
            description:
              - Pre-defined type of credential.
            type: str
            required: false
          credential:
            description:
              - Basic authentication credential (username / password) for the vCenter server.
            type: dict
            required: false
            suboptions:
              username:
                description:
                  - Username required for the basic auth scheme.
                  - Minimum length is 3 characters and maximum length is 256 characters.
                type: str
                required: true
              password:
                description:
                  - Password required for the basic auth scheme.
                type: str
                required: true
      intersight:
        description:
          - Cisco Intersight credential using API key based authentication.
        type: dict
        required: false
        suboptions:
          url:
            description:
              - Intersight connection URL.
            type: str
            required: true
          deployment_type:
            description:
              - Type of Intersight connection.
            type: str
            required: true
            choices:
              - INTERSIGHT_SAAS
              - INTERSIGHT_VIRTUAL_APPLIANCE
          type:
            description:
              - Pre-defined type of credential.
            type: str
            required: false
          credential:
            description:
              - Key based authentication credential for Cisco Intersight.
            type: dict
            required: false
            suboptions:
              api_key:
                description:
                  - Intersight connection API key.
                type: str
                required: true
              secret_key:
                description:
                  - Intersight connection secret key.
                type: str
                required: true
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
- name: Create BMC credential
  nutanix.ncp.ntnx_credential_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bmc_credential_ansible"
    credential_details:
      bmc:
        credential:
          username: "ADMIN"
          password: "BmcSecret.123"
  register: result
  ignore_errors: true

- name: Create vCenter credential
  nutanix.ncp.ntnx_credential_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vcenter_credential_ansible"
    credential_details:
      vcenter:
        address:
          fqdn:
            value: "vcenter.example.com"
        credential:
          username: "administrator@vsphere.local"
          password: "VcenterSecret.123"
  register: result
  ignore_errors: true

- name: Create Intersight credential
  nutanix.ncp.ntnx_credential_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "intersight_credential_ansible"
    credential_details:
      intersight:
        url: "https://intersight.com/api/v1/"
        deployment_type: "INTERSIGHT_SAAS"
        credential:
          api_key: "5f7a1e2b3c4d5e6f7a8b9c0d/6e7f8a9b0c1d2e3f4a5b6c7d/6e7f8a9b0c1d2e3f4a5b6c7d"
          secret_key: "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEE...==\n-----END EC PRIVATE KEY-----"
  register: result
  ignore_errors: true

- name: Update BMC credential (rotate password)
  nutanix.ncp.ntnx_credential_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "bmc_credential_ansible"
    credential_details:
      bmc:
        credential:
          username: "ADMIN"
          password: "BmcSecret.456"
  register: result
  ignore_errors: true

- name: Delete credential
  nutanix.ncp.ntnx_credential_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a credential.
    - If the operation is create or update and C(wait) is true, it will return the credential details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "credential_details": {
          "credential": {
              "password": null,
              "username": "ADMIN"
          },
          "type": null
      },
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "is_valid": true,
      "links": null,
      "name": "bmc_credential_ansible",
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
    - The external ID of the credential.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: always
  type: bool
  sample: false

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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Credential with ext_id:2e40ff57-20aa-4d2b-b179-298db969c20d will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_credentials_api_instance,
    get_etag,
)
from ..module_utils.v4.security.helpers import get_credential_by_ext_id  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_security_py_client as security_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as security_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    basic_auth_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    key_based_auth_spec = dict(
        api_key=dict(type="str", required=True, no_log=True),
        secret_key=dict(type="str", required=True, no_log=True),
    )

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    ip_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=security_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=security_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=security_sdk.FQDN,
        ),
    )

    bmc_credential_spec = dict(
        type=dict(type="str", required=False),
        credential=dict(
            type="dict",
            options=basic_auth_spec,
            obj=security_sdk.BasicAuth,
            no_log=False,
        ),
    )

    vcenter_credential_spec = dict(
        address=dict(
            type="dict",
            options=ip_or_fqdn_spec,
            required=True,
            obj=security_sdk.IPAddressOrFQDN,
        ),
        type=dict(type="str", required=False),
        credential=dict(
            type="dict",
            options=basic_auth_spec,
            obj=security_sdk.BasicAuth,
            no_log=False,
        ),
    )

    intersight_credential_spec = dict(
        url=dict(type="str", required=True),
        deployment_type=dict(
            type="str",
            required=True,
            choices=["INTERSIGHT_SAAS", "INTERSIGHT_VIRTUAL_APPLIANCE"],
        ),
        type=dict(type="str", required=False),
        credential=dict(
            type="dict",
            options=key_based_auth_spec,
            obj=security_sdk.KeyBasedAuth,
            no_log=False,
        ),
    )

    credential_details_obj_map = {
        "bmc": security_sdk.BmcCredential,
        "vcenter": security_sdk.VcenterCredential,
        "intersight": security_sdk.IntersightCredential,
    }

    credential_details_spec = dict(
        bmc=dict(
            type="dict",
            options=bmc_credential_spec,
            no_log=False,
        ),
        vcenter=dict(
            type="dict",
            options=vcenter_credential_spec,
            no_log=False,
        ),
        intersight=dict(
            type="dict",
            options=intersight_credential_spec,
            no_log=False,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        credential_details=dict(
            type="dict",
            options=credential_details_spec,
            obj=credential_details_obj_map,
            mutually_exclusive=[("bmc", "vcenter", "intersight")],
            required_one_of=[("bmc", "vcenter", "intersight")],
            no_log=False,
        ),
    )
    return module_args


def _build_credential_spec(module, result, msg):
    """Build a Credential SDK spec from the current module params."""

    sg = SpecGenerator(module)
    default_spec = security_sdk.Credential()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg=msg, **result)
    return spec


def _resolve_credential_ext_id_from_task(task):
    """Return the credential ext_id from a task response.

    The Credentials service reports the newly created / updated credential
    inside the task's ``completion_details`` list under the name ``resourceId``.
    Fall back to ``entities_affected`` for deployments that use that shape.
    """

    ext_id = get_ext_id_from_task_completion_details(task, name="resourceId")
    if ext_id:
        return ext_id
    ext_id = get_entity_ext_id_from_task(
        task, rel=TASK_CONSTANTS.RelEntityType.CREDENTIAL
    )
    if ext_id:
        return ext_id
    return get_entity_ext_id_from_task(task, rel=None)


def create_credential(module, api_instance, result):
    validate_required_params(module, ["name", "credential_details"])

    spec = _build_credential_spec(
        module, result, "Failed generating create Credential spec"
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_credential(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Credential",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = _resolve_credential_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            fetched = get_credential_by_ext_id(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def _user_supplied_secret(module):
    """Return True when the user's params include any secret material.

    Secret material (``password`` / ``api_key`` / ``secret_key``) is never
    returned by the API, so an update that supplies a secret cannot be
    reliably detected as idempotent — the safest behaviour is to send it to
    the API and let the server accept or reject the write.
    """

    details = module.params.get("credential_details") or {}
    for key in ("bmc", "vcenter", "intersight"):
        block = details.get(key) or {}
        cred = block.get("credential") or {}
        for sensitive in ("password", "api_key", "secret_key"):
            if cred.get(sensitive) not in (None, ""):
                return True
    return False


def check_credential_idempotency(old_spec, update_spec):
    """Compare current and desired credential specs, ignoring server-computed fields.

    The API never returns secret material (password / api_key / secret_key) and
    also does not return the plain username for BasicAuth-based credentials.
    We must therefore strip these fields from BOTH sides before comparing so a
    legitimate no-op update (e.g. re-running the same play with all
    non-secret fields unchanged AND no secret material supplied) can be
    detected as idempotent.
    """

    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)

    for attr in ("is_valid", "links", "tenant_id", "ext_id"):
        old_spec.pop(attr, None)
        update_spec.pop(attr, None)

    def _clean(details):
        if not isinstance(details, dict):
            return
        # The `type` field at the credential_details level acts as the
        # polymorphic discriminator: the API returns the fully-qualified SDK
        # class name (e.g. ``security.v4.config.BmcCredential``) while the
        # user supplies the short enum (e.g. ``BMC``). Skip it entirely.
        details.pop("type", None)
        cred = details.get("credential")
        if isinstance(cred, dict):
            for sensitive in ("password", "api_key", "secret_key", "username"):
                cred.pop(sensitive, None)
            # After stripping unreturned secret material the credential dict
            # is often empty on one side but present on the other; treat both
            # empty and missing as the same for idempotency purposes.
            if not any(v is not None for v in cred.values()):
                details.pop("credential", None)
        elif cred is None:
            details.pop("credential", None)

    _clean(old_spec.get("credential_details"))
    _clean(update_spec.get("credential_details"))

    return old_spec == update_spec


def update_credential(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["credential_details"])

    current_spec = get_credential_by_ext_id(module, api_instance, ext_id)

    update_spec = _build_credential_spec(
        module, result, "Failed generating Credential update spec"
    )

    if check_credential_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ) and not _user_supplied_secret(module):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Credential", **result
        )

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_credential_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Credential",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetched = get_credential_by_ext_id(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_credential(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Credential with ext_id:{0} will be deleted.".format(ext_id)
        return

    current = get_credential_by_ext_id(module, api_instance, ext_id)
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for deleting Credential", **result
        )

    try:
        resp = api_instance.delete_credential_by_id(extId=ext_id, if_match=etag)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Credential",
        )

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
        if module.params.get("wait"):
            task_status = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_credentials_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_credential(module, api_instance, result)
        else:
            create_credential(module, api_instance, result)
    else:
        delete_credential(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
