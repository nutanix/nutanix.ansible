#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clusters_info
short_description: ndb clusters info module
version_added: 1.8.0-beta.1
description: 'Get clusters info'
options:
      name:
        description:
            - cluster name
        type: str
      uuid:
        description:
            - cluster id
        type: str
      filters:
        description:
            - write
        type: dict
        suboptions:
            include_management_server:
                description:
                    - write
                type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.clusters import Cluster  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        include_management_server=dict(type="bool"),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
        ),
    )

    return module_args


def get_cluster(module, result):
    cluster = Cluster(module)
    if module.params.get("name"):
        name = module.params["name"]
        resp, err = cluster.get_cluster(name=name)
    else:
        uuid = module.params["uuid"]
        resp, err = cluster.get_cluster(uuid=uuid)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching cluster info", **result)
    result["response"] = resp


def get_clusters(module, result):
    cluster = Cluster(module)
    cluster.filters_map()
    query_params = module.params.get("filters")

    resp = cluster.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("name", "uuid"),
            ("name", "filters"),
            ("uuid", "filters"),
        ],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_cluster(module, result)
    else:
        get_clusters(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
