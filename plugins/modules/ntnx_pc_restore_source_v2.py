#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_restore_source_v2
short_description: Creates or Deletes a restore source pointing to a cluster or object store to restore the domain manager.
version_added: 2.1.0
description:
    - Creates or Deletes a restore source pointing to a cluster or object store to restore the domain manager.
    - The created restore source is intended to be deleted after use.
    - If the restore source is not deleted using the deleteRestoreSource API, then it is auto-deleted after sometime.
options:
    state:
        description:
            - If C(present), will create a restore source.
            - If C(absent), will delete a restore source.
        type: str
        required: False
        choices:
            - present
            - absent
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: False
        default: True
    location:
        description:
            - Location of the backup target.
            - For example, a cluster or an object store endpoint, such as AWS s3.
        type: dict
        required: true
        suboptions:
            cluster_location:
                description: Location of the cluster.
                type: dict
                suboptions:
                    config:
                        description: Configuration of the Cluster reference of the remote cluster to be connected.
                        type: dict
                        required: true
                        suboptions:
                            ext_id:
                                description: External ID of the remote cluster.
                                type: str
                                required: true
            object_store_location:
                description: Location of the object store.
                type: dict
                suboptions:
                    provider_config:
                        description: The base model of S3 object store endpoint where domain manager is backed up.
                        type: dict
                        required: true
                        suboptions:
                            bucket_name:
                                description: The bucket name of the object store endpoint where backup data of domain manager is to be stored.
                                type: str
                                required: true
                            region:
                                description: The region name of the object store endpoint where backup data of domain manager is stored.
                                type: str
                                default: us-east-1
                            credentials:
                                description: Secret credentials model for the object store containing access key ID and secret access key.
                                type: dict
                                required: false
                                suboptions:
                                    access_key_id:
                                        description: Access key Id for the object store provided for backup target.
                                        type: str
                                        required: true
                                    secret_access_key:
                                        description: Secret access key for the object store provided for backup target.
                                        type: str
                                        required: true
                    backup_policy:
                        description: Backup policy for the object store provided.
                        type: dict
                        suboptions:
                            rpo_in_minutes:
                                description: RPO interval in minutes at which the backup will be taken
                                type: int
                                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

from ..module_utils.v4.prism.spec.pc import PrismSpecs as prism_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = prism_specs.get_location_backup_spec()
    return module_args


def create_restore_source(module, domain_manager_backups_api, result):
    """
    This method will create restore source.
    Args:
        module (object): Ansible module object
        domain_manager_backups_api (object): DomainManagerBackupApi instance
        result (dict): Result object
    """
    sg = SpecGenerator(module)
    default_spec = prism_sdk.RestoreSource()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore source spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = domain_manager_backups_api.create_restore_source(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating restore source",
        )
    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_restore_source(module, domain_manager_backups_api, result):
    """
    This method will delete restore source.
    Args:
        module (object): Ansible module object
        domain_manager_backups_api (object): DomainManagerBackupApi instance
        result (dict): Result object
    """
    ext_id = module.params.get("ext_id")
    resp = None
    try:
        resp = domain_manager_backups_api.delete_restore_source_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting restore source",
        )
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }

    state = module.params.get("state")
    prsim = get_domain_manager_backup_api_instance(module)
    if state == "present":
        create_restore_source(module, prsim, result)
    else:
        delete_restore_source(module, prsim, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
