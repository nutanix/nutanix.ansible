#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_profile_association_v2
short_description: Module to associate or disassociate cluster profile with a cluster.
version_added: 2.4.0
description:
  - This module can be used to associate or disassociate cluster profile with a cluster in Nutanix Prism Central.
  - Associate cluster profile with a cluster will apply the cluster profile configuration to the cluster.
  - Disassociate cluster profile from a cluster will remove the cluster profile external ID from the cluster, which means that cluster is no longer
    associated with the cluster profile and any changes made to the cluster profile configuration will not be applied to the cluster.
  - This module will not remove the cluster profile configuration from the cluster.
  - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - The state of the cluster profile association.
            - If C(present), the module will associate the cluster profile with the cluster.
            - If C(absent), the module will disassociate the cluster profile from the cluster.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external identifier of the cluster profile
            - Required when associating or disassociating a cluster profile.
        type: str
        required: true
    clusters:
        description:
            - Cluster reference for an entity.
        type: list
        elements: dict
        required: true
        suboptions:
            uuid:
                description:
                    - The external identifier of the cluster.
                    - Required when associating or disassociating a cluster profile.
                type: str
                required: true
    dryrun:
        description:
          - If set to true, the module will only run prechecks and will not apply the cluster profile configuration to the cluster.
          - If set to false which is the default value, the module will apply the cluster profile configuration to the cluster.
          - This parameter is only applicable when the state is present (associate cluster profile with a cluster).
        type: bool
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Associate cluster profile with cluster
  nutanix.ncp.ntnx_clusters_profile_association_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    clusters:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result

- name: Disassociate cluster profile from cluster
  nutanix.ncp.ntnx_clusters_profile_association_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    state: absent
    clusters:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result
"""
RETURN = r"""
response:
    description: Task response for associating or disassociating cluster profiles with a cluster.
    type: dict
    returned: always
    sample:
        {
            "app_name": null,
            "cluster_ext_ids": [
                "000642d8-a2e0-e442-0b82-606eab989991"
            ],
            "completed_time": "2025-11-05T13:23:32.384983+00:00",
            "completion_details": null,
            "created_time": "2025-11-05T13:21:50.094877+00:00",
            "entities_affected": [
                {
                    "ext_id": "e5a0f246-0880-44f2-7b51-0aad170ac45e",
                    "name": "cluster_profile_1_2",
                    "rel": "clustermgmt:config:cluster-profile"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:2bf53fdd-309b-5971-9f4b-436c86e8f92f",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-11-05T13:23:32.384982+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 12,
            "operation": "applyClusterProfile",
            "operation_description": "Apply Cluster Profile",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "resource_links": null,
            "root_task": null,
            "started_time": "2025-11-05T13:21:50.525912+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:03832fb1-ff0e-4074-5829-0c116803d528",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:03832fb1-ff0e-4074-5829-0c116803d528",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:070dd938-dd47-4a0b-50b3-196da96cb65d",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:070dd938-dd47-4a0b-50b3-196da96cb65d",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:17b09ddf-aa52-4108-6133-05fb4f3d6346",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:17b09ddf-aa52-4108-6133-05fb4f3d6346",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:1ddb0485-91dd-4981-4c54-42edc480865a",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:1ddb0485-91dd-4981-4c54-42edc480865a",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:3b5786a2-414c-4272-52e1-ea6a95be1755",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:3b5786a2-414c-4272-52e1-ea6a95be1755",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:431af0df-3a29-411f-6e21-da52cabcecca",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:431af0df-3a29-411f-6e21-da52cabcecca",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:485bcb73-4370-472e-42d0-eecfd51e25f4",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:485bcb73-4370-472e-42d0-eecfd51e25f4",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:5fda5caa-3356-41a0-446f-45f1a40fe959",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:5fda5caa-3356-41a0-446f-45f1a40fe959",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:8df580b1-9010-4881-7500-f881781c195d",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:8df580b1-9010-4881-7500-f881781c195d",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:ba3b4da5-1ea8-4f55-7489-bee373b35437",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:ba3b4da5-1ea8-4f55-7489-bee373b35437",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:ba8d024a-7e75-49c0-6d7a-57472cf5973e",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:ba8d024a-7e75-49c0-6d7a-57472cf5973e",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:c7f63002-950b-42b4-613f-8a261f4ca105",
                    "href": "https://10.98.145.91:9440/api/prism/v4.1/config/tasks/ZXJnb24=:c7f63002-950b-42b4-613f-8a261f4ca105",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

task_ext_id:
    description: The external identifier of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:2cdebadf-10c5-4538-9da6-cb7700e79fbe"

ext_id:
    description: The external identifier of the cluster profile.
    type: str
    returned: always
    sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while associating cluster profile"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_profiles_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    clusters_spec = dict(
        uuid=dict(type="str", required=True),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        clusters=dict(
            type="list",
            elements="dict",
            options=clusters_spec,
            obj=clusters_sdk.ClusterReference,
            required=True,
        ),
        dryrun=dict(type="bool", default=False),
    )

    return module_args


def associate_cluster_profile(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = clusters_sdk.ClusterReferenceListSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster profile spec for associating cluster profile with a cluster.",
            **result  # fmt: skip
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    dry_run = module.params.get("dryrun", False)
    resp = None
    try:
        resp = cluster_profiles.apply_cluster_profile(
            extId=ext_id, body=spec, _dryrun=dry_run
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating cluster profile",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    if module.params.get("dryrun", False):
        result["changed"] = False
    else:
        result["changed"] = True


def disassociate_cluster_profile(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = clusters_sdk.ClusterReferenceListSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster profile spec for disassociating cluster profile from a cluster.",
            **result  # fmt: skip
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = cluster_profiles.disassociate_cluster_from_cluster_profile(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating cluster profile",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
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
        "error": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    cluster_profiles = get_cluster_profiles_api_instance(module)
    if state == "present":
        associate_cluster_profile(module, cluster_profiles, result)
    else:
        disassociate_cluster_profile(module, cluster_profiles, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
