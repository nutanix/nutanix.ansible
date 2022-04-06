# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (
    Foundation,
)

__metaclass__ = type


class EnumerateAOSPackages(Foundation):
    def __init__(self, module):
        resource_type = "/enumerate_nos_packages"
        super(EnumerateAOSPackages, self).__init__(module, resource_type=resource_type)

    def list(self):
        resp = self.read()
        return resp
