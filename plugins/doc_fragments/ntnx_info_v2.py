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
"""
