# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .base_module import NdbBaseModule

__metaclass__ = type


class NdbBaseInfoModule(NdbBaseModule):
    def __init__(self, **kwargs):
        self.argument_spec = deepcopy(NdbBaseModule.argument_spec)
        self.argument_spec.pop("state")
        self.argument_spec.pop("wait")
        self.argument_spec.pop("timeout")
        super(NdbBaseInfoModule, self).__init__(**kwargs)
