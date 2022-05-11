# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx CRUD opperations
    DOCUMENTATION = r"""
options:
  state:
    description:
      - Specify state
      - If C(state) is set to C(present) then the opperation will be  create the item
      - >-
        If C(state) is set to C(absent) and if the item exists, then
        item is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for the  CRUD operation to complete.
    type: bool
    required: false
    default: True
"""
