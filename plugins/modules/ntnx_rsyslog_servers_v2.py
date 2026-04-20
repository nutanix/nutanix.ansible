#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_rsyslog_servers_v2
short_description: Create, Update, Delete RSYSLOG server configurations in Nutanix clusters
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete RSYSLOG server configurations on a Nutanix cluster.
  - RSYSLOG is used for collecting, filtering, parsing, and forwarding logs from Nutanix components such as CVMs and PCVMs to external remote rsyslog servers.
  - It allows users to specify exactly which Nutanix modules (such as AUDIT, CALM, PRISM, etc.)
    should forward their logs and filter them by specific severity levels (such as EMERGENCY, NOTICE, INFO, etc.).
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create an RSYSLOG server) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Update an RSYSLOG server) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Delete an RSYSLOG server) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create an RSYSLOG server.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the RSYSLOG server.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the RSYSLOG server.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - The external ID of the cluster on which to manage the RSYSLOG server.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the RSYSLOG server.
      - Required for update and delete operations.
    type: str
    required: false
  server_name:
    description:
      - The name of the RSYSLOG server.
      - Required for create and update operations.
    type: str
    required: false
  ip_address:
    description:
      - The IP address of the RSYSLOG server.
      - Required for create and update operations.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the RSYSLOG server.
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
              - Prefix length of the network.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the RSYSLOG server.
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
              - Prefix length of the IPv6 network.
            type: int
            required: false
            default: 128
  port:
    description:
      - The port of the RSYSLOG server.
      - Required for create and update operations.
    type: int
    required: false
  network_protocol:
    description:
      - The network protocol to use for the RSYSLOG server.
      - Required for create and update operations.
    type: str
    required: false
    choices:
      - UDP
      - TCP
      - RELP
  modules:
    description:
      - List of module items to forward logs for.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the module.
        type: str
        required: true
        choices:
          - ACROPOLIS
          - API_AUDIT
          - APLOS
          - AUDIT
          - CALM
          - CASSANDRA
          - CEREBRO
          - CURATOR
          - EPSILON
          - FLOW
          - FLOW_SERVICE_LOGS
          - GENESIS
          - LAZAN
          - LCM
          - MINERVA_CVM
          - NCM_AIOPS
          - PRISM
          - STARGATE
          - SYSLOG_MODULE
          - UHARA
          - ZOOKEEPER
      log_severity_level:
        description:
          - The log severity level for the module.
        type: str
        required: true
        choices:
          - EMERGENCY
          - ALERT
          - CRITICAL
          - ERROR
          - WARNING
          - NOTICE
          - INFO
          - DEBUG
      should_log_monitor_files:
        description:
          - Whether to log monitor files for the module.
        type: bool
        default: true
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create RSYSLOG server
  nutanix.ncp.ntnx_rsyslog_servers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    server_name: "rsyslog_server_1"
    ip_address:
      ipv4:
        value: "192.168.1.100"
    port: 514
    network_protocol: "UDP"
    modules:
      - name: "PRISM"
        log_severity_level: "INFO"
        should_log_monitor_files: false
  register: result
  ignore_errors: true

- name: Update RSYSLOG server
  nutanix.ncp.ntnx_rsyslog_servers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    server_name: "rsyslog_server_1"
    ip_address:
      ipv4:
        value: "192.168.1.101"
    port: 515
    network_protocol: "TCP"
    modules:
      - name: "PRISM"
        log_severity_level: "DEBUG"
  register: result
  ignore_errors: true

- name: Delete RSYSLOG server
  nutanix.ncp.ntnx_rsyslog_servers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting an RSYSLOG server.
    - If the operation is create or delete and C(wait) is true, it will return the task details.
    - If the operation is update and C(wait) is true, it will return the RSYSLOG server details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "server_name": "rsyslog_server_1",
      "ip_address": {
          "ipv4": {
              "value": "192.168.1.100",
              "prefix_length": 32
          },
          "ipv6": null
      },
      "port": 514,
      "network_protocol": "UDP",
      "modules": [
          {
              "name": "PRISM",
              "log_severity_level": "INFO",
              "should_log_monitor_files": false
          }
      ],
      "links": null,
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the RSYSLOG server.
  returned: when the RSYSLOG server is created or updated
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: In idempotent operations
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
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
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_rsyslog_server  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=clustermgmt_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=clustermgmt_sdk.IPv6Address,
        ),
    )

    module_item_spec = dict(
        name=dict(
            type="str",
            required=True,
            choices=[
                "ACROPOLIS",
                "API_AUDIT",
                "APLOS",
                "AUDIT",
                "CALM",
                "CASSANDRA",
                "CEREBRO",
                "CURATOR",
                "EPSILON",
                "FLOW",
                "FLOW_SERVICE_LOGS",
                "GENESIS",
                "LAZAN",
                "LCM",
                "MINERVA_CVM",
                "NCM_AIOPS",
                "PRISM",
                "STARGATE",
                "SYSLOG_MODULE",
                "UHARA",
                "ZOOKEEPER",
            ],
            obj=clustermgmt_sdk.RsyslogModuleName,
        ),
        log_severity_level=dict(
            type="str",
            required=True,
            choices=[
                "EMERGENCY",
                "ALERT",
                "CRITICAL",
                "ERROR",
                "WARNING",
                "NOTICE",
                "INFO",
                "DEBUG",
            ],
            obj=clustermgmt_sdk.RsyslogModuleLogSeverityLevel,
        ),
        should_log_monitor_files=dict(type="bool", required=False, default=True),
    )

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        server_name=dict(type="str", required=False),
        ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=clustermgmt_sdk.IPAddress,
        ),
        port=dict(type="int", required=False),
        network_protocol=dict(
            type="str",
            required=False,
            choices=["UDP", "TCP", "RELP"],
            obj=clustermgmt_sdk.RsyslogNetworkProtocol,
        ),
        modules=dict(
            type="list",
            elements="dict",
            options=module_item_spec,
            required=False,
            obj=clustermgmt_sdk.RsyslogModuleItem,
        ),
    )
    return module_args


def create_rsyslog_server(module, api_instance, cluster_ext_id, result):
    validate_required_params(
        module, ["server_name", "ip_address", "port", "network_protocol"]
    )
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.RsyslogServer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create RSYSLOG server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    try:
        resp = api_instance.create_rsyslog_server(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating RSYSLOG server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(old_spec, update_spec):
    old_dict = strip_internal_attributes(old_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())
    return old_dict == update_dict


def update_rsyslog_server(module, api_instance, cluster_ext_id, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_rsyslog_server(module, api_instance, cluster_ext_id, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update RSYSLOG server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    try:
        resp = api_instance.update_rsyslog_server_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating RSYSLOG server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_rsyslog_server(module, api_instance, cluster_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_rsyslog_server(module, api_instance, cluster_ext_id, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "RSYSLOG server with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_rsyslog_server_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting RSYSLOG server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
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
        "error": None,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    state = module.params.get("state")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    if state == "absent":
        delete_rsyslog_server(module, api_instance, cluster_ext_id, result)
    elif module.params.get("ext_id"):
        update_rsyslog_server(module, api_instance, cluster_ext_id, result)
    else:
        create_rsyslog_server(module, api_instance, cluster_ext_id, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
