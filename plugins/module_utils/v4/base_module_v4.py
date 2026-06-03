# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..base_module import BaseModule

__metaclass__ = type


class BaseModuleV4(BaseModule):
    """
    Base module class for Nutanix PC v4 based modules
    """

    proxy_argument_spec = dict(
        https_proxy=dict(type="str"),
        http_proxy=dict(type="str"),
        all_proxy=dict(type="str"),
        no_proxy=dict(type="str"),
        proxy_username=dict(type="str"),
        proxy_password=dict(type="str", no_log=True),
    )

    def __init__(self, **kwargs):
        if "argument_spec" not in self.__dict__:
            self.argument_spec = deepcopy(BaseModule.argument_spec)
        self.argument_spec.update(deepcopy(self.proxy_argument_spec))
        self.argument_spec.update(
            read_timeout=dict(type="int", default=30000),
        )
        super(BaseModuleV4, self).__init__(**kwargs)
