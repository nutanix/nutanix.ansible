# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text


def get_hostname(compose_func, host_vars, hostnames, default_name, strict=False):
    """
    Evaluate Jinja2 hostname expressions against host_vars.
    Returns the first non-empty result, or default_name as fallback.
    """
    for preference in hostnames:
        try:
            hostname = compose_func(preference, host_vars)
        except Exception as e:
            if strict:
                raise AnsibleError(
                    "Could not compose '%s' as hostname - %s" % (preference, to_text(e))
                )
            continue
        if hostname:
            return to_text(hostname)
    return default_name
