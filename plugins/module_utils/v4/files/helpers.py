# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_replication_policy(module, api_instance, ext_id):
    """
    Fetch a single replication policy by its external ID.

    Args:
        module (AnsibleModule): The Ansible module.
        api_instance (ntnx_files_py_client.ReplicationPoliciesApi): SDK API
            instance created via ``get_replication_policies_api_instance``.
        ext_id (str): External ID of the replication policy.

    Returns:
        ntnx_files_py_client.ReplicationPolicy: The replication policy object
        (``.data`` payload of the SDK response). ``raise_api_exception`` is
        called and the module is failed if the SDK raises.
    """
    try:
        return api_instance.get_replication_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching replication policy info using ext_id",
        )


def get_vdi_user_session(
    module, api_instance, file_server_ext_id, replication_policy_ext_id, ext_id
):
    """
    Fetch a single VDI synchronization user session under a replication policy.

    Args:
        module (AnsibleModule): The Ansible module.
        api_instance (ntnx_files_py_client.ReplicationPoliciesApi): SDK API
            instance.
        file_server_ext_id (str): External ID of the owning file server.
        replication_policy_ext_id (str): External ID of the VDI-sync
            replication policy the session belongs to.
        ext_id (str): External ID of the VDI user session.

    Returns:
        ntnx_files_py_client.VdiUserSession: The user session object.
    """
    try:
        return api_instance.get_vdi_user_session_by_id(
            fileServerExtId=file_server_ext_id,
            replicationPolicyExtId=replication_policy_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VDI user session info using ext_id",
        )
