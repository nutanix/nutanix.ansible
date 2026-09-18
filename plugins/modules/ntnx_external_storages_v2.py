#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_storages_v2
short_description: Create and update external storages in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and update external storages in Nutanix Prism Central.
  - An external storage represents a third-party storage provider (for example Dell PowerFlex,
    Everpure FlashArray or Dell PowerStore) that is connected to an AOS cluster.
  - If C(state) is C(present) and C(ext_id) is not provided, an external storage is created.
  - If C(state) is C(present) and C(ext_id) is provided, the external storage is updated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create an External Storage) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - >-
    B(Update an External Storage) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - The referenced AOS cluster (C(cluster_ext_id)) must already exist and be registered to Prism Central
    before creating an external storage against it.
  - The C(provider_type) and C(cluster_ext_id) cannot be modified after creation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create external storage.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update external storage.
      - If C(state) is set to C(absent) then the module will report that delete is not supported by the API.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the external storage.
      - Required for the update operation.
    type: str
    required: false
  name:
    description:
      - Name of the external storage.
      - Maximum 75 characters.
      - Required for the create operation.
    type: str
    required: false
  provider_type:
    description:
      - The type of external storage provider.
      - Required for the create operation.
      - This value cannot be modified after creation.
    type: str
    required: false
    choices:
      - DELL_POWERFLEX
      - EVERPURE_FLASHARRAY
      - DELL_POWERSTORE
  cluster_ext_id:
    description:
      - The UUID of the AOS cluster connected to this external storage.
      - Required for the create operation.
      - This value cannot be modified after creation.
    type: str
    required: false
  end_point_address:
    description:
      - The endpoint address (IP or FQDN) of the external storage provider.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - The IPv4 address of the endpoint.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the IPv4 address.
            type: int
            required: false
      ipv6:
        description:
          - The IPv6 address of the endpoint.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the IPv6 address.
            type: int
            required: false
      fqdn:
        description:
          - The fully qualified domain name of the endpoint.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The FQDN value.
            type: str
            required: true
  config:
    description:
      - Configuration details for the external storage.
      - Exactly one provider configuration must be supplied and it must match C(provider_type).
      - The configuration type cannot be changed after creation, but certain attributes within may be updated.
    type: dict
    required: false
    suboptions:
      dell_powerflex:
        description:
          - Configuration for a Dell PowerFlex external storage provider.
          - Use with C(provider_type=DELL_POWERFLEX).
        type: dict
        required: false
        suboptions:
          system_id:
            description:
              - The Dell PowerFlex system identifier.
              - Maximum 256 characters.
            type: str
            required: false
          username:
            description:
              - Username to connect to the external storage.
              - Maximum 256 characters.
            type: str
            required: false
          password:
            description:
              - Password to connect to the external storage.
              - Maximum 256 characters.
            type: str
            required: false
          protection_domain_name:
            description:
              - The name of the protection domain from which the storage pool is created.
              - This value cannot be modified after creation.
              - Maximum 256 characters.
            type: str
            required: false
          storage_pool_name:
            description:
              - The storage pool name from Dell PowerFlex Manager.
              - This value cannot be modified after creation.
              - Maximum 256 characters.
            type: str
            required: false
          storage_pool_id:
            description:
              - Unique identifier for the Dell PowerFlex storage pool.
              - Maximum 256 characters.
            type: str
            required: false
      everpure_flasharray:
        description:
          - Configuration for an Everpure FlashArray external storage provider.
          - Use with C(provider_type=EVERPURE_FLASHARRAY).
        type: dict
        required: false
        suboptions:
          id:
            description:
              - The Everpure FlashArray identifier.
              - Maximum 256 characters.
            type: str
            required: false
          username:
            description:
              - Username to connect to the external storage.
              - Maximum 256 characters.
            type: str
            required: false
          password:
            description:
              - Password to connect to the external storage.
              - Maximum 256 characters.
            type: str
            required: false
          realm_name:
            description:
              - The name of the realm the Everpure FlashArray pod is associated with.
              - This value cannot be modified after creation.
              - Maximum 256 characters.
            type: str
            required: false
          pod_name:
            description:
              - Name of the Everpure FlashArray pod.
              - This value cannot be modified after creation.
              - Maximum 256 characters.
            type: str
            required: false
          pod_id:
            description:
              - Unique identifier for the Everpure FlashArray pod.
              - Maximum 256 characters.
            type: str
            required: false
      dell_powerstore:
        description:
          - Configuration for a Dell PowerStore external storage provider.
          - Use with C(provider_type=DELL_POWERSTORE).
        type: dict
        required: false
        suboptions:
          username:
            description:
              - Username to connect to the external storage.
              - Maximum 256 characters.
            type: str
            required: false
          password:
            description:
              - Password to connect to the external storage.
              - Maximum 256 characters.
            type: str
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
- name: Create external storage with Dell PowerFlex provider
  nutanix.ncp.ntnx_external_storages_v2:
    state: present
    name: "external_storage_ansible"
    provider_type: "DELL_POWERFLEX"
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    end_point_address:
      ipv4:
        value: "10.44.76.100"
    config:
      dell_powerflex:
        system_id: "powerflex-system-01"
        username: "admin"
        password: "PowerFlex.123"
        protection_domain_name: "pd-01"
        storage_pool_name: "sp-01"
        storage_pool_id: "sp-id-01"
  register: result
  ignore_errors: true

- name: Update external storage credentials
  nutanix.ncp.ntnx_external_storages_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "external_storage_ansible_updated"
    provider_type: "DELL_POWERFLEX"
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    end_point_address:
      ipv4:
        value: "10.44.76.101"
    config:
      dell_powerflex:
        system_id: "powerflex-system-01"
        username: "admin"
        password: "PowerFlex.456"
        protection_domain_name: "pd-01"
        storage_pool_name: "sp-01"
        storage_pool_id: "sp-id-01"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or updating external storage.
    - If the operation is create or update and C(wait) is true, it will return the external storage details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "config": {
        "protection_domain_name": "pd-01",
        "storage_pool_id": "sp-id-01",
        "storage_pool_name": "sp-01",
        "system_id": "powerflex-system-01",
        "username": "admin"
      },
      "end_point_address": {
        "fqdn": null,
        "ipv4": {
          "prefix_length": 32,
          "value": "10.44.76.100"
        },
        "ipv6": null
      },
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "free_capacity_bytes": null,
      "health": null,
      "links": null,
      "name": "external_storage_ansible",
      "owner_ext_id": null,
      "provider_type": "DELL_POWERFLEX",
      "tenant_id": null,
      "total_capacity_bytes": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the external storage.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped, for example during idempotency checks.
  returned: when applicable
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent, check mode, or an unsupported operation is requested.
  type: str
  sample: "Api Exception raised while creating external storage"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_external_storages_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_external_storage  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Mapping of provider_type enum values to the config sub-key and SDK config class.
PROVIDER_CONFIG_MAP = {
    "DELL_POWERFLEX": ("dell_powerflex", "DellPowerFlexConfig"),
    "EVERPURE_FLASHARRAY": ("everpure_flasharray", "EverpureFlashArrayConfig"),
    "DELL_POWERSTORE": ("dell_powerstore", "DellPowerStoreConfig"),
}


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    end_point_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=clustermgmt_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=clustermgmt_sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=clustermgmt_sdk.FQDN,
            required=False,
        ),
    )

    dell_powerflex_spec = dict(
        system_id=dict(type="str", required=False),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        protection_domain_name=dict(type="str", required=False),
        storage_pool_name=dict(type="str", required=False),
        storage_pool_id=dict(type="str", required=False),
    )

    everpure_flasharray_spec = dict(
        id=dict(type="str", required=False),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        realm_name=dict(type="str", required=False),
        pod_name=dict(type="str", required=False),
        pod_id=dict(type="str", required=False),
    )

    dell_powerstore_spec = dict(
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
    )

    config_spec = dict(
        dell_powerflex=dict(
            type="dict",
            options=dell_powerflex_spec,
            required=False,
        ),
        everpure_flasharray=dict(
            type="dict",
            options=everpure_flasharray_spec,
            required=False,
        ),
        dell_powerstore=dict(
            type="dict",
            options=dell_powerstore_spec,
            required=False,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        provider_type=dict(
            type="str",
            required=False,
            choices=["DELL_POWERFLEX", "EVERPURE_FLASHARRAY", "DELL_POWERSTORE"],
        ),
        cluster_ext_id=dict(type="str", required=False),
        end_point_address=dict(
            type="dict",
            options=end_point_address_spec,
            obj=clustermgmt_sdk.IPAddressOrFQDN,
            required=False,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
        ),
        config=dict(
            type="dict",
            options=config_spec,
            required=False,
            mutually_exclusive=[
                ("dell_powerflex", "everpure_flasharray", "dell_powerstore")
            ],
        ),
    )
    return module_args


def _build_config_spec(module, result, provider_type):
    """Build the provider specific external storage config SDK object.

    Args:
        module: Ansible module.
        result (dict): result dict populated on failure.
        provider_type (str): the selected external storage provider type.
    Returns:
        object|None: the provider config SDK object, or None if no config was supplied.
    """
    config = module.params.get("config")
    if not config:
        return None

    sub_key, sdk_class_name = PROVIDER_CONFIG_MAP.get(provider_type, (None, None))
    if sub_key is None:
        module.fail_json(
            msg="Unsupported provider_type '{0}' for external storage config".format(
                provider_type
            ),
            **result,
        )

    provider_config = config.get(sub_key)
    if not provider_config:
        module.fail_json(
            msg="config.{0} must be provided when provider_type is '{1}'".format(
                sub_key, provider_type
            ),
            **result,
        )

    sdk_class = getattr(clustermgmt_sdk, sdk_class_name)
    config_obj = sdk_class()
    for attr, value in provider_config.items():
        if value is not None:
            setattr(config_obj, attr, value)
    return config_obj


def _remove_read_only_attributes(spec):
    """Null out server-computed / read-only attributes before an API call.

    The external storage API rejects read-only fields (for example providerType,
    which is inferred from the config discriminator) if they are present in the
    request body. Capacity and health are also server-populated on GET.
    """
    spec.provider_type = None
    spec.total_capacity_bytes = None
    spec.free_capacity_bytes = None
    spec.health = None
    return spec


def create_external_storage(module, api_instance, result):
    validate_required_params(module, ["name", "provider_type", "cluster_ext_id"])

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.ExternalStorage()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create external storage spec", **result)

    spec.config = _build_config_spec(module, result, module.params.get("provider_type"))

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # providerType is a read-only field derived from the config discriminator.
    _remove_read_only_attributes(spec)

    resp = None
    try:
        resp = api_instance.create_external_storage(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating external storage",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.EXTERNAL_STORAGE
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_external_storage(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_idempotency(old_spec, update_spec):
    """Return True if the update spec matches the current spec (nothing to change)."""
    return old_spec == update_spec


def update_external_storage(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_external_storage(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating external storage", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update external storage spec", **result)

    if module.params.get("config"):
        provider_type = module.params.get("provider_type") or getattr(
            current_spec, "provider_type", None
        )
        update_spec.config = _build_config_spec(module, result, provider_type)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # providerType (and other server-computed fields) are read-only on update.
    _remove_read_only_attributes(update_spec)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_external_storage_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating external storage",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_external_storage(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_external_storage(module, api_instance, result):
    """External storage does not support delete via the v4 API.

    The clustermgmt v4.3 ExternalStorages API exposes only Create, Get, List and
    Update operations. There is no delete endpoint, so we fail with a clear message
    instead of silently succeeding.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    module.fail_json(
        msg=(
            "Delete operation is not supported for external storages by the "
            "clustermgmt v4 API."
        ),
        **result,
    )


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
    api_instance = get_external_storages_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_external_storage(module, api_instance, result)
        else:
            create_external_storage(module, api_instance, result)
    else:
        delete_external_storage(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
