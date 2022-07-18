# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type

from .prism import Prism


class UserGroups(Prism):
    def __init__(self, module):
        resource_type = "/user_groups"
        super(UserGroups, self).__init__(module, resource_type=resource_type)


def get_user_group_reference_spec(uuid=None):
    return deepcopy({"kind": "user_group", "uuid": uuid})
