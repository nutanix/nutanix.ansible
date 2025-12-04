#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ssl_certificates_info_v2
short_description: Provides detailed information about the SSL certificate for specific cluster
version_added: 2.4.0
description:
  - This module provides detailed information about the SSL certificate for specific cluster.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the cluster.
      - Mandatory for fetching the SSL certificates for specific cluster.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: fetch SSL certificates info using cluster external ID
  nutanix.ncp.ntnx_ssl_certificates_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
  register: result
"""

RETURN = r"""
response:
  description: Response for fetching SSL certificates info for specific cluster.
  type: dict
  returned: always
  sample:
    {
      "ca_chain": null,
      "passphrase": null,
      "private_key": null,
      "private_key_algorithm": "RSA_2048",
      "public_certificate": "-----BEGIN CERTIFICATE-----\n
        Sm9zZTEUMBIGA1UEChMLTnV0YW5peCBJbmMxLzAtBgNVBAsTJlNlY3VyaXR5IEVu\n
        Udlp55wEPI7s28oycJgT39Q7x95F2BJkIfyC70n6KgxWXyQtuJ6cxd1c0NcYZsEx\nnpVZBA==\n
        -----END CERTIFICATE-----"
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the cluster.
  type: str
  returned: always
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_ssl_certificates_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_ssl_certificates  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_ssl_certificates_info(module, result):
    ssl_certificates = get_ssl_certificates_api_instance(module)
    cluster_ext_id = module.params.get("ext_id")
    resp = get_ssl_certificates(module, ssl_certificates, cluster_ext_id)
    result["ext_id"] = cluster_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    get_ssl_certificates_info(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
