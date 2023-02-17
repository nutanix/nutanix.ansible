# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx AutomatedPatchingSpec
    DOCUMENTATION = r"""
options:
    automated_patching:
        description:
            - write
        type: dict
        suboptions:
            maintenance_window:
                description:
                    - write
                type: dict
                suboptions:
                    name:
                        description:
                            - write
                        type: str
                    uuid:
                        description:
                            - write
                        type: str
            tasks:
                description:
                    - write
                type: list
                elements: dict
                suboptions:
                    type:
                        description:
                            - write
                        type: str
                        choices: ["OS_PATCHING", "DB_PATCHING"]
                    pre_task_cmd:
                        description:
                            - write
                        type: str
                    post_task_cmd:
                        description:
                            - write
                        type: str
"""
