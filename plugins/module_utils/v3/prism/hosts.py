# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Host(Prism):
    def __init__(self, module):
        resource_type = "/hosts"
        super(Host, self).__init__(module, resource_type=resource_type)
