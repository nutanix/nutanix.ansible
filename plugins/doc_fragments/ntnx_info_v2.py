# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx files info
    DOCUMENTATION = r"""
options:
  filter:
    description:
      - The filter in OData syntax used for the results
    type: str
  page:
    description:
      - The number of page
    type: int
  limit:
    description:
      - The number of records
    type: int
  orderby:
    description:
      - The sort order in which results are returned
    type: str
  select:
    description:
      - The attribute name to select
    type: str
  fetch_all:
    description:
      - When C(true), paginate through the list API until all available entities
        are returned (ignores C(page); C(limit) is used as the page size when set).
      - When C(false), return a single page using the API default page size (50)
        unless C(limit)/C(page) are set — this is the current listing behavior.
      - Does not apply when fetching a single entity by C(ext_id).
    type: bool
    required: false
    default: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
"""
