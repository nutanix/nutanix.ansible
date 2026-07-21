#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_artifact_files_info_v2
short_description: Fetch report ArtifactFile info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ArtifactFile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ArtifactFile.
  - If C(ext_id) is not provided, list multiple ArtifactFile optionally
    filtered / paginated using standard v4 info parameters.
  - The opsmgmt v4 API does not expose a dedicated get-by-ID endpoint for
    report artifacts, so C(ext_id) is resolved server-side using an OData
    filter on the list endpoint.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the Nutanix IAM privileges to view report
    artifacts. Typical required roles are Prism Admin, Prism Viewer,
    Super Admin, or a custom role that carries the
    C(OpsMgmt:View_Report_Artifact_File) operation permission.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  ext_id:
    description:
      - The external ID of the report artifact to fetch.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch a specific report artifact by external ID
  nutanix.ncp.ntnx_artifact_files_info_v2:
    ext_id: "7e3d1c17-4e49-4397-4b0f-00cd0debb46c"
  register: artifact_by_id

- name: List all report artifacts
  nutanix.ncp.ntnx_artifact_files_info_v2:
  register: all_artifacts

- name: List report artifacts of type LOGO using an OData filter
  nutanix.ncp.ntnx_artifact_files_info_v2:
    filter: "type eq Opsmgmt.Config.ArtifactType'LOGO'"
  register: logo_artifacts

- name: List the first report artifact only
  nutanix.ncp.ntnx_artifact_files_info_v2:
    limit: 1
  register: first_artifact
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ArtifactFile info v4 API.
    - It can be a single ArtifactFile if external ID is provided.
    - List of multiple ArtifactFile if external ID is not provided with
      optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "7e3d1c17-4e49-4397-4b0f-00cd0debb46c",
        "file_type": "PNG",
        "links": null,
        "tenant_id": null,
        "type": "LOGO"
      }
    ]

total_available_results:
  description:
    - Total number of report artifacts available on the server for the
      current query, as reported by the API metadata block.
  type: int
  returned: when all report artifacts are fetched
  sample: 1

ext_id:
  description:
    - The external ID of the report artifact when a single entity is
      fetched.
  type: str
  returned: when single entity
  sample: "7e3d1c17-4e49-4397-4b0f-00cd0debb46c"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching report artifacts info"

error:
  description:
    - This field typically holds information about if the task have
      errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description:
    - This field typically holds information about if the task have
      failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.content.api_client import (  # noqa: E402
    get_report_artifacts_api_instance,
)
from ..module_utils.v4.content.helpers import get_report_artifact  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_report_artifact_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    artifact = get_report_artifact(module, api_instance, ext_id)
    if artifact is None:
        module.fail_json(
            msg=(
                "Report artifact with ext_id '{0}' was not found on the "
                "Prism Central endpoint.".format(ext_id)
            ),
            **result,
        )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(artifact.to_dict())


def get_report_artifacts(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating report artifacts info spec", **result)

    kwargs.pop("_orderby", None)

    try:
        resp = api_instance.list_report_artifacts(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report artifacts info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_report_artifacts_api_instance(module)
    if module.params.get("ext_id"):
        get_report_artifact_using_ext_id(module, api_instance, result)
    else:
        get_report_artifacts(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
