# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx files CRUD operations
    DOCUMENTATION = r"""
options:
  nutanix_debug:
        description:
            - Enable detailed debug logging for all API calls made by this module.
            - When enabled, logs will include HTTP method, URL, headers, request body, response body, status code, and elapsed time.
            - Authorization headers and sensitive information are automatically redacted.
            - This parameter can also be set via the NUTANIX_DEBUG environment variable and is preferred over the NUTANIX_DEBUG environment variable.
        type: bool
        required: false
        default: false
  nutanix_log_file:
        description:
            - The file to write the logs to.
            - This parameter can also be set via the NUTANIX_LOG_FILE environment variable and is preferred over the NUTANIX_LOG_FILE environment variable.
        type: str
        required: false
        default: /tmp/nutanix_ansible_debug.log
"""
