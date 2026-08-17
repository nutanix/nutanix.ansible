#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_artifacts_info_v2
short_description: Fetch report artifacts info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ReportArtifact in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ReportArtifact.
  - If C(ext_id) is not provided, list multiple ReportArtifact optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get report artifact by ext_id) -
      Required Roles: Consumer, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, NCM Admin, Intelligent Ops Admin
    - >-
      B(List Report Artifacts) -
      Required Roles: Consumer, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, NCM Admin, Intelligent Ops Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  ext_id:
    description:
      - The external ID of the report artifact.
      - When provided the module returns the single matching artifact.
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
- name: Get report artifact using ext_id
  nutanix.ncp.ntnx_report_artifacts_info_v2:
    ext_id: "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11"
  register: result

- name: List all report artifacts
  nutanix.ncp.ntnx_report_artifacts_info_v2:
  register: result

- name: List report artifacts with filter
  nutanix.ncp.ntnx_report_artifacts_info_v2:
    filter: "type eq 'LOGO'"
  register: result

- name: List report artifacts with limit
  nutanix.ncp.ntnx_report_artifacts_info_v2:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReportArtifact info v4 API.
    - It can be a single ReportArtifact if external ID is provided.
    - List of multiple ReportArtifact if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11",
      "file_type": "PNG",
      "links": null,
      "tenant_id": null,
      "type": "LOGO"
    }

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
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the report artifact
  type: str
  returned: when external ID is provided
  sample: "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11"

total_available_results:
  description: The total number of available report artifacts in PC.
  type: int
  returned: when all report artifacts are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_report_artifacts_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import (  # noqa: E402
    get_report_artifact_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Argument spec for :module:`ntnx_report_artifacts_info_v2`.

    Only ``ext_id`` is entity-specific; the OData query parameters
    (``filter``, ``limit``, ``page``, ``orderby``, ``select``) are
    inherited from :class:`BaseInfoModule`.
    """
    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_report_artifact_using_ext_id(module, api_instance, result):
    """
    Return a single ReportArtifact identified by ``ext_id``.

    Fails with a descriptive message when no artifact has the requested
    ``ext_id`` (the underlying list-with-filter call succeeded but
    yielded no match).
    """
    ext_id = module.params.get("ext_id")
    artifact = get_report_artifact_by_ext_id(module, api_instance, ext_id)
    if artifact is None:
        module.fail_json(
            msg="ReportArtifact with ext_id:'{0}' not found.".format(ext_id),
            **result,
        )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(artifact.to_dict())


def get_report_artifacts(module, api_instance, result):
    """
    List report artifacts, honoring the OData query params (``filter``,
    ``limit``, ``page``, ``orderby``, ``select``) from the info spec.

    The API's ``total_available_results`` is surfaced verbatim so
    playbooks can paginate. If the API returns no matches ``response`` is
    forced to an empty list — never ``None`` — so playbook filters
    downstream (``| length``) do not blow up.
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating report artifacts info spec", **result)

    try:
        resp = api_instance.list_report_artifacts(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report artifacts info",
        )
        return

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    """
    Entry point: build the info module, dispatch on presence of
    ``ext_id`` (single vs. list flow) and return the result.
    """
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
