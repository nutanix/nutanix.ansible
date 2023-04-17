# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from nutanix_files import NutanixFiles



class Share(NutanixFiles):
    resource_type = "/config/file-servers"

    def __init__(self, module):

        super(Share, self).__init__(module, self.resource_type)
        self.build_spec_methods = {}