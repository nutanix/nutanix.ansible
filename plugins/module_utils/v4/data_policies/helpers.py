#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_protection_policy(module, api_instance, ext_id):
    """
    This method will return protection policy info using external ID.
    Args:
        module: Ansible module
        api_instance: ProtectionPoliciesApi instance from ntnx_datapolicies_py_clien sdk
        ext_id (str): top level recovery point external ID
    Returns:
        protection_policy_info (object): protection policy info
    """
    try:
        return api_instance.get_protection_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching protection policy info using ext_id",
        )
