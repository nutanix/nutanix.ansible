# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ..module_utils.base_module import BaseModule

__metaclass__ = type


class BaseInfoModule(BaseModule):

    info_argument_spec = dict(
        offset=dict(type="int"), length=dict(type="int"), filter=dict(type="str")
    )

    def __init__(self, **kwargs):
        BaseModule.argument_spec.pop("state")
        BaseModule.argument_spec.pop("wait")
        BaseModule.argument_spec.update(self.info_argument_spec)
        super(BaseInfoModule, self).__init__(**kwargs)
