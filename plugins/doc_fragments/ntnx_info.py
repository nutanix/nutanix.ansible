# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx credentials
    DOCUMENTATION = r"""
options:
  sort_order:
    description:
      - The sort order in which results are returned
    type: str
  sort_attribute:
    description:
      - The attribute to perform sort on
    type: str
  offset:
    description:
      - Offset from the start of the entity list
    type: int
  length:
    description:
      - The number of records to retrieve relative to the offset
    type: int
  filter:
    description:
      - The filter in key-value syntax used for the results
    type: dict
  custom_filter:
    description:
      - The filter in key-value syntax used for the results
    type: dict
  filter_string:
    description:
      - The filter in FIQL syntax used for the results
    type: str
"""
