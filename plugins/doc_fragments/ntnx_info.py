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
      - The sorting order of the list assending or dessinding
    type: str
  sort_attribute:
    description:
      - Sort the list by specfic attribute
    type: str
  offset:
    description:
      - The offset to start searching the list
    type: int
  length:
    description:
      - The length of the element in the list
    type: int
  filter:
    description:
      - Refine The Search list by given filter
    type: str
"""
