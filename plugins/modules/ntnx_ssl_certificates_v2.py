#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ssl_certificates_v2
short_description: Update SSL certificates for a specific cluster in Nutanix Prism Central
description:
    - This module allows you to update the SSL certificate for a specific cluster
    - Certificate payload should be in Base64 format
    - This module uses PC v4 APIs based SDKs
version_added: 2.4.0
options:
  ext_id:
    description:
      - The external ID of the cluster.
    type: str
    required: true
  passphrase:
    description:
      - Passphrase used to decrypt private keys.
    type: str
    required: false
  private_key:
    description:
      - Private key in Base64 format.
    type: str
    required: false
  public_certificate:
    description:
      - Public certificate in Base64 format.
    type: str
    required: false
  ca_chain:
    description:
      - CA chain (Certificate Authority chain) in Base64 format.
    type: str
    required: false
  private_key_algorithm:
    description:
      - Private Key Algorithm used for SSL certificate.
    type: str
    required: true
    choices:
    - ECDSA_256
    - JKS
    - RSA_2048
    - ECDSA_521
    - KRB_KEYTAB
    - PKCS12
    - RSA_4096
    - RSA_PUBLIC
    - ECDSA_384
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Update SSL certificate for a specific cluster
  nutanix.ncp.ntnx_ssl_certificates_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: <cluster_ext_id>
    passphrase: <passphrase>
    private_key: <private_key>
    public_certificate: <public_certificate>
    ca_chain: <ca_chain>
    private_key_algorithm: <private_key_algorithm>
"""

RETURN = r"""
response:
    description:
        - Response for updating SSL certificate for a specific cluster.
        - Task details if C(wait) is false.
        - SSL certificate details if C(wait) is true.
    type: dict
    returned: always
    sample:

task_ext_id:
    description:
        - Task external ID.
    type: str
    returned: always
    sample: ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1
ext_id:
    description:
        - External ID of the cluster.
    type: str
    returned: always
    sample: 00064079-9b02-8c5e-185b-ac1f6b6f97e2
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_ssl_certificates_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_ssl_certificates  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        passphrase=dict(type="str", required=False, no_log=True),
        private_key=dict(type="str", required=False, no_log=True),
        public_certificate=dict(type="str", required=False),
        ca_chain=dict(type="str", required=False),
        private_key_algorithm=dict(
            type="str",
            required=True,
            choices=[
                "ECDSA_256",
                "JKS",
                "RSA_2048",
                "ECDSA_521",
                "KRB_KEYTAB",
                "PKCS12",
                "RSA_4096",
                "RSA_PUBLIC",
                "ECDSA_384",
            ],
        ),
    )
    return module_args


def update_ssl_certificates(module, result):
    ssl_certificates_api = get_ssl_certificates_api_instance(module)
    cluster_ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.SSLCertificate()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create ssl certificates spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_ssl_certificates(module, ssl_certificates_api, cluster_ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating ssl certificates", **result
        )

    kwargs = {"if_match": etag}
    resp = None

    try:
        resp = ssl_certificates_api.update_ssl_certificate(
            body=spec, clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while updating ssl certificates for the cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.SSL_CERTIFICATES
        )
        if ext_id:
            resp = get_ssl_certificates(module, ssl_certificates_api, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    update_ssl_certificates(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
