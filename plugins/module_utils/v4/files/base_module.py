# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type

from ...base_module import BaseModule


class FilesBaseModule(BaseModule):
    def __init__(self, **kwargs):
        argument_spec = deepcopy(self.argument_spec)
        argument_spec["timeout"] = dict(type="int", required=False, default=60 * 60)
        if kwargs.get("argument_spec"):
            argument_spec.update(deepcopy(kwargs["argument_spec"]))

        kwargs["argument_spec"] = argument_spec
        super(FilesBaseModule, self).__init__(**kwargs)
