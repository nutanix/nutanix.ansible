#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_tags_info
short_description: info module for ndb tags info
version_added: 1.9.0
description: info module for ndb tags
options:
      uuid:
        description:
            - tags uuid
        type: str
      name:
        description:
            - get tags based on name
            - since there can be multiple tags with same name,
              use C(entity_type) in C(filters) to get correct tag info
        type: str
      filters:
        description:
            - filters spec
        type: dict
        suboptions:
            entity_type:
                description:
                    - get all tags based on entity_type
                type: str
                choices: ["DATABASE","CLONE","TIME_MACHINE","DATABASE_SERVER",]
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_info_base_module
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: get all tags
  ntnx_ndb_tags_info:
  register: result

- name: get tag based on uuid
  ntnx_ndb_tags_info:
    uuid: "{{database_tag_uuid}}"
  register: result

- name: get all tags based on DATABASE entity type
  ntnx_ndb_tags_info:
    filters:
      entity_type: "DATABASE"
  register: result

- name: get all tags based on CLONE entity type
  ntnx_ndb_tags_info:
    filters:
      entity_type: "CLONE"
  register: result

- name: get tag based on DATABASE entity type and name
  ntnx_ndb_tags_info:
    filters:
      entity_type: "DATABASE"
    name: "tag_name"
  register: result
"""

RETURN = r"""
response:
  description: listing all tags
  returned: only when name and uuid is not used for fetching specific tag
  type: list
  sample: [
            {
                "dateCreated": "2023-02-24 08:14:05",
                "dateModified": "2023-02-24 08:14:05",
                "entityType": "DATABASE",
                "id": "aba66aab-e73e-40c3-92bc-fabd2b449475",
                "name": "ansible-databases",
                "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "required": false,
                "status": "ENABLED",
                "values": 2
            },
            {
                "dateCreated": "2023-02-24 08:13:48",
                "dateModified": "2023-02-24 08:13:48",
                "entityType": "CLONE",
                "id": "ca15bae2-cf47-4b64-829f-30a1f6f55b62",
                "name": "ansible-clones",
                "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "required": false,
                "status": "ENABLED",
                "values": 0
            },
        ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.tags import Tag  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        entity_type=dict(
            type="str",
            choices=[
                "DATABASE",
                "TIME_MACHINE",
                "CLONE",
                "DATABASE_SERVER",
            ],
        ),
    )

    module_args = dict(
        uuid=dict(type="str"),
        name=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
        ),
    )

    return module_args


def format_tags_filters(filters):
    """
    This routine returns filter spec with attribute name changes as acceptable by api
    """
    attrs = {"entity_type": "entityType"}

    updated_filters = {}
    for key in filters.keys():
        if attrs.get(key):
            updated_filters[attrs.get(key)] = filters[key]
    return updated_filters


def get_tags(module, result):
    tags = Tag(module)
    filters = module.params.get("filters")
    if filters:
        filters = format_tags_filters(filters)

    # fetch tag using uuid
    if module.params.get("uuid"):
        resp = tags.read(uuid=module.params.get("uuid"))

    # fetch tag using name and entity type (optional)
    elif module.params.get("name"):
        entity_type = filters.get("entityType")
        uuid, err = tags.get_tag_uuid(
            name=module.params.get("name"), entity_type=entity_type
        )
        if err:
            result["error"] = err
            return module.fail_json(msg="Failed fetching tag info", **result)
        resp = tags.read(uuid=uuid)

    # fetch all tags
    else:
        resp = tags.read(query=filters)

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("uuid", "filters")],
    )
    result = {"changed": False, "error": None, "response": None}
    get_tags(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
