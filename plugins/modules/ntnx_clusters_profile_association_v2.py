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
            ext_id:
                description:
                    - The external identifier of the cluster.
                    - Required when associating or disassociating a cluster profile.
                type: str
                required: true
    dryrun:
    description:
      - Whether to run prechecks only.
    type: bool
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
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
        ext_id=dict(type="str", required=True),
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
        dry_run=dict(type="bool", default=False),
    )

    return module_args


def associate_cluster_profile(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = clusters_sdk.ClusterReference()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster profile spec for association", **result
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
    default_spec = clusters_sdk.ClusterReference()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster profile spec for disassociation", **result
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
