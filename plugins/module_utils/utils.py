# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def remove_param_with_none_value(d):
    for k, v in d.copy().items():
        if v is None:
            d.pop(k)
        elif isinstance(v, dict):
            remove_param_with_none_value(v)
        elif isinstance(v, list):
            for e in v:
                if isinstance(e, dict):
                    remove_param_with_none_value(e)
                else:
                    break


def intersection(first_obj, second_obj):
    if isinstance(first_obj, dict):
        for key, value in first_obj.items():
            if key in second_obj and second_obj[key] == value:
                return True
            if isinstance(value, (dict, list)):
                if intersection(value, second_obj):
                    return True

    elif isinstance(first_obj, list):
        for item in first_obj:
            if intersection(item, second_obj):
                return True
    return False
