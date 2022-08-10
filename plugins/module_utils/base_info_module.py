# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..module_utils.base_module import BaseModule

__metaclass__ = type


class BaseInfoModule(BaseModule):
    info_argument_spec = dict(
        offset=dict(type="int"),
        length=dict(type="int"),
        filter=dict(type="dict"),
        custom_filter=dict(type="dict"),
    )

    def __init__(self, skip_info_args=False, **kwargs):
        self.argument_spec = deepcopy(BaseModule.argument_spec)
        self.argument_spec.pop("state")
        self.argument_spec.pop("wait")
        if not skip_info_args:
            self.argument_spec.update(self.info_argument_spec)
        super(BaseInfoModule, self).__init__(**kwargs)
