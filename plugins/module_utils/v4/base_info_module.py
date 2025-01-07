# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..base_module import BaseModule

__metaclass__ = type


class BaseInfoModule(BaseModule):
    """
    Base Info module class for Nutanix PC v4 list APIs based modules
    """

    info_argument_spec = dict(
        filter=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
        orderby=dict(type="str"),
        select=dict(type="str"),
    )

    def __init__(self, skip_info_args=False, **kwargs):
        self.argument_spec = deepcopy(BaseModule.argument_spec)
        self.argument_spec.pop("state")
        self.argument_spec.pop("wait")
        if not skip_info_args:
            self.argument_spec.update(self.info_argument_spec)
        super(BaseInfoModule, self).__init__(**kwargs)
