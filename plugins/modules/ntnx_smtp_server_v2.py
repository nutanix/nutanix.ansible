#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_smtp_server_v2
short_description: Create, Update and Delete SMTP server in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Create, Update and Delete SMTP server configuration in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create SMTP server) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - >-
      B(Update SMTP server) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - >-
      B(Delete SMTP server) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create SMTP server.
            - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update SMTP server.
            - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete SMTP server.
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID of the SMTP server configuration.
            - Required for update and delete operations.
        type: str
        required: false
    domain_manager_ext_id:
        description:
            - The external identifier of the domain manager (Prism Central) resource.
            - Required for all operations.
        type: str
        required: true
    is_active:
        description:
            - Whether this SMTP server configuration is active.
        type: bool
        required: false
        default: true
    config:
        description:
            - Configuration for the SMTP server used to send alert emails.
            - Supports Basic Auth, XOAUTH2, and Microsoft Graph protocols.
        type: dict
        required: false
        config_details:
            description:
                - Exactly one of the protocol configurations must be provided.
            type: dict
            required: true
            suboptions:
                    basic_auth:
                        description:
                            - SMTP configuration for Basic Auth protocol, requiring username and password for authentication.
                        type: dict
                        required: false
                        suboptions:
                            security_mode:
                                description:
                                    - The transport-layer security mode for the SMTP connection.
                                type: str
                                required: true
                                choices:
                                    - NONE
                                    - SSL
                                    - STARTTLS
                            host:
                                description:
                                    - SMTP host address. Can be IP or FQDN.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description:
                                            - An IPv4 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv4 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length of the network.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description:
                                            - An IPv6 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv6 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length of the network.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description:
                                            - A fully qualified domain name.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The fully qualified domain name value.
                                                type: str
                                                required: true
                            port:
                                description:
                                    - TCP port number of the SMTP server.
                                type: int
                                required: false
                                default: 25
                            email_address:
                                description:
                                    - The email address that appears as the sender in alert emails.
                                type: str
                                required: false
                            username:
                                description:
                                    - Username for authenticating with the SMTP server using Basic Auth.
                                type: str
                                required: false
                            password:
                                description:
                                    - Password for authenticating with the SMTP server using Basic Auth.
                                type: str
                                required: false
                    xoauth2:
                        description:
                            - SMTP configuration for the XOAUTH2 protocol, using OAuth 2.0 for token-based SMTP authentication.
                        type: dict
                        required: false
                        suboptions:
                            security_mode:
                                description:
                                    - The transport-layer security mode for the SMTP connection.
                                type: str
                                required: true
                                choices:
                                    - NONE
                                    - SSL
                                    - STARTTLS
                            tenant_id:
                                description:
                                    - The Azure AD tenant identifier for OAuth 2.0 authentication.
                                type: str
                                required: true
                            client_id:
                                description:
                                    - The application client ID registered in the identity provider.
                                type: str
                                required: true
                            token_endpoint:
                                description:
                                    - The OAuth 2.0 token endpoint URL used to obtain an access token.
                                type: str
                                required: true
                            scope:
                                description:
                                    - The OAuth 2.0 scope requested when acquiring an access token.
                                type: str
                                required: true
                            host:
                                description:
                                    - SMTP host address.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description:
                                            - An IPv4 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv4 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length of the network.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description:
                                            - An IPv6 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv6 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length of the network.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description:
                                            - A fully qualified domain name.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The fully qualified domain name value.
                                                type: str
                                                required: true
                            port:
                                description:
                                    - TCP port number of the SMTP server.
                                type: int
                                required: true
                                default: 25
                            email_address:
                                description:
                                    - The email address that appears as the sender in alert emails.
                                type: str
                                required: true
                            expiry_time:
                                description:
                                    - The expiry date-time of the client credentials.
                                type: str
                                required: false
                            oauth_credentials:
                                description:
                                    - OAuth 2.0 credentials used for token acquisition.
                                type: dict
                                required: true
                                suboptions:
                                    client_secret:
                                        description:
                                            - OAuth 2.0 client secret credentials for token acquisition.
                                        type: dict
                                        required: false
                                        suboptions:
                                            client_secret:
                                                description:
                                                    - The client secret value.
                                                type: str
                                                required: true
                                    certificate:
                                        description:
                                            - Certificate-based OAuth 2.0 credentials.
                                        type: dict
                                        required: false
                                        suboptions:
                                            private_key:
                                                description:
                                                    - The private key used for certificate-based OAuth 2.0 authentication.
                                                type: str
                                                required: true
                                            public_cert:
                                                description:
                                                    - The public certificate used for certificate-based OAuth 2.0 authentication.
                                                type: str
                                                required: true
                                            private_key_passphrase:
                                                description:
                                                    - Passphrase to decrypt the private key.
                                                type: str
                                                required: false
                                            thumbprint:
                                                description:
                                                    - The certificate thumbprint.
                                                type: str
                                                required: false
                    graph:
                        description:
                            - Configuration for sending emails via Microsoft Graph API.
                        type: dict
                        required: false
                        suboptions:
                            tenant_id:
                                description:
                                    - The Azure AD tenant identifier for OAuth 2.0 authentication.
                                type: str
                                required: true
                            client_id:
                                description:
                                    - The application client ID registered in the identity provider.
                                type: str
                                required: true
                            token_endpoint:
                                description:
                                    - The OAuth 2.0 token endpoint URL used to obtain an access token.
                                type: str
                                required: false
                            scope:
                                description:
                                    - The OAuth 2.0 scope requested when acquiring an access token.
                                type: str
                                required: false
                                default: "https://graph.microsoft.com/.default"
                            email_address:
                                description:
                                    - The email address that appears as the sender in alert emails.
                                type: str
                                required: true
                            expiry_time:
                                description:
                                    - The expiry date-time of the client credentials.
                                type: str
                                required: false
                            oauth_credentials:
                                description:
                                    - OAuth 2.0 credentials used for token acquisition.
                                type: dict
                                required: true
                                suboptions:
                                    client_secret:
                                        description:
                                            - OAuth 2.0 client secret credentials for token acquisition.
                                        type: dict
                                        required: false
                                        suboptions:
                                            client_secret:
                                                description:
                                                    - The client secret value.
                                                type: str
                                                required: true
                                    certificate:
                                        description:
                                            - Certificate-based OAuth 2.0 credentials.
                                        type: dict
                                        required: false
                                        suboptions:
                                            private_key:
                                                description:
                                                    - The private key used for certificate-based OAuth 2.0 authentication.
                                                type: str
                                                required: true
                                            public_cert:
                                                description:
                                                    - The public certificate used for certificate-based OAuth 2.0 authentication.
                                                type: str
                                                required: true
                                            private_key_passphrase:
                                                description:
                                                    - Passphrase to decrypt the private key.
                                                type: str
                                                required: false
                                            thumbprint:
                                                description:
                                                    - The certificate thumbprint.
                                                type: str
                                                required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create SMTP server with Basic Auth
  nutanix.ncp.ntnx_smtp_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    is_active: true
    config:
      basic_auth:
        security_mode: "NONE"
        host:
          fqdn:
            value: "smtp.example.com"
        port: 25
        email_address: "nutanix@example.com"
        username: "smtp_user"
        password: "smtp_pass"
  register: result
  ignore_errors: true

- name: Update SMTP server
  nutanix.ncp.ntnx_smtp_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    ext_id: "11111111-1111-1111-1111-111111111111"
    is_active: true
    config:
      basic_auth:
        security_mode: "STARTTLS"
        host:
          fqdn:
            value: "smtp.example.com"
        port: 587
        email_address: "nutanix@example.com"
        username: "smtp_user"
        password: "smtp_pass_updated"
  register: result
  ignore_errors: true

- name: Delete SMTP server
  nutanix.ncp.ntnx_smtp_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    ext_id: "11111111-1111-1111-1111-111111111111"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for creating, updating, or deleting SMTP server.
      - If C(wait) is true and the operation is Create or Update, it will contain the SMTP server details.
      - If C(wait) is false or the operation is Delete, it will contain the task details.
  returned: always
  type: dict
  sample:
    {
        "config": {
            "config_details": {
                "email_address": "nutanix@example.com",
                "host": {
                    "fqdn": {
                        "value": "smtp.example.com"
                    },
                    "ipv4": null,
                    "ipv6": null
                },
                "password": null,
                "port": 25,
                "security_mode": "NONE",
                "username": "smtp_user"
            }
        },
        "email_notification_status": null,
        "ext_id": "11111111-1111-1111-1111-111111111111",
        "is_active": true,
        "links": null,
        "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the SMTP server.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while creating SMTP server"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import get_smtp_server  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_etag,
    get_smtp_server_api_instance,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_FIELDS = ["email_notification_status", "links", "tenant_id"]


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=prism_sdk.FQDN),
    )

    client_secret_spec = dict(
        client_secret=dict(type="str", required=True, no_log=True),
    )

    certificate_spec = dict(
        private_key=dict(type="str", required=True, no_log=True),
        public_cert=dict(type="str", required=True, no_log=True),
        private_key_passphrase=dict(type="str", required=False, no_log=True),
        thumbprint=dict(type="str", required=False),
    )

    oauth_credentials_spec = dict(
        client_secret=dict(
            type="dict",
            options=client_secret_spec,
            obj=prism_sdk.ClientSecretCredentials,
        ),
        certificate=dict(
            type="dict",
            options=certificate_spec,
            obj=prism_sdk.CertificateCredentials,
        ),
    )

    oauth_wrapper_spec = dict(
        credentials_details=dict(
            type="dict",
            options=oauth_credentials_spec,
            obj={
                "client_secret": prism_sdk.ClientSecretCredentials,
                "certificate": prism_sdk.CertificateCredentials,
            },
        ),
    )

    basic_auth_spec = dict(
        security_mode=dict(
            type="str",
            required=True,
            choices=["NONE", "SSL", "STARTTLS"],
            obj=prism_sdk.SmtpSecurityMode,
        ),
        host=dict(
            type="dict",
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int", required=False),
        email_address=dict(type="str", required=False),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
    )

    xoauth2_spec = dict(
        security_mode=dict(
            type="str",
            required=True,
            choices=["NONE", "SSL", "STARTTLS"],
            obj=prism_sdk.SmtpSecurityMode,
        ),
        tenant_id=dict(type="str", required=True),
        client_id=dict(type="str", required=True),
        token_endpoint=dict(type="str", required=True),
        scope=dict(type="str", required=True),
        host=dict(
            type="dict",
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int", required=True),
        email_address=dict(type="str", required=True),
        expiry_time=dict(type="str", required=False),
        oauth_credentials=dict(
            type="dict",
            required=True,
            options=oauth_wrapper_spec,
            obj=prism_sdk.OAuthCredentials,
        ),
    )

    graph_spec = dict(
        tenant_id=dict(type="str", required=True),
        client_id=dict(type="str", required=True),
        token_endpoint=dict(type="str", required=False),
        scope=dict(type="str", required=False),
        email_address=dict(type="str", required=True),
        expiry_time=dict(type="str", required=False),
        oauth_credentials=dict(
            type="dict",
            required=True,
            options=oauth_wrapper_spec,
            obj=prism_sdk.OAuthCredentials,
        ),
    )

    smtp_config_details_spec = dict(
        basic_auth=dict(
            type="dict",
            options=basic_auth_spec,
            obj=prism_sdk.BasicAuthSmtpConfig,
        ),
        xoauth2=dict(
            type="dict",
            options=xoauth2_spec,
            obj=prism_sdk.Xoauth2SmtpConfig,
        ),
        graph=dict(
            type="dict",
            options=graph_spec,
            obj=prism_sdk.GraphSmtpConfig,
        ),
    )

    smtp_config_spec = dict(
        config_details=dict(
            type="dict",
            options=smtp_config_details_spec,
            obj={
                "basic_auth": prism_sdk.BasicAuthSmtpConfig,
                "xoauth2": prism_sdk.Xoauth2SmtpConfig,
                "graph": prism_sdk.GraphSmtpConfig,
            },
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str", required=True),
        is_active=dict(type="bool", required=False, default=True),
        config=dict(
            type="dict",
            options=smtp_config_spec,
            obj=prism_sdk.SmtpConfig,
        ),
    )
    return module_args


def create_smtp_server(module, result, api_instance):
    validate_required_params(module, ["domain_manager_ext_id", "config"])
    sg = SpecGenerator(module)
    default_spec = prism_sdk.SmtpServer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create SMTP server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    resp = None
    try:
        resp = api_instance.create_smtp_server(
            domainManagerExtId=domain_manager_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating SMTP server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.SMTP_SERVER
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_smtp_server(module, api_instance, domain_manager_ext_id, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for SMTP Server"
                ),
                msg="Failed to get entity ext_id from task for SMTP Server",
            )
    result["changed"] = True


def check_smtp_server_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    # remove read-only fields that may differ
    for key in READ_ONLY_FIELDS:
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_smtp_server(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    result["ext_id"] = ext_id
    old_spec = get_smtp_server(module, api_instance, domain_manager_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update SMTP server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_smtp_server_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_smtp_server_by_id(
            domainManagerExtId=domain_manager_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SMTP server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_smtp_server(module, api_instance, domain_manager_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_smtp_server(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "SMTP server with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_smtp_server_by_id(
            domainManagerExtId=domain_manager_ext_id,
            extId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting SMTP server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("config", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_smtp_server_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_smtp_server(module, result, api_instance)
        else:
            create_smtp_server(module, result, api_instance)
    else:
        delete_smtp_server(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
