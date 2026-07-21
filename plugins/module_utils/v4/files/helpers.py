# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_vdi_user_session(
    module, api_instance, file_server_ext_id, replication_policy_ext_id, ext_id
):
    """
    Return the VDI synchronization user session that matches the supplied
    triple of external identifiers. The Nutanix Files v4 API requires all
    three IDs (file server, replication policy, user session) to uniquely
    address a session, so callers must supply all of them.

    Args:
        module (object): Ansible module object.
        api_instance (object): ReplicationPoliciesApi instance from
            ntnx_files_py_client sdk.
        file_server_ext_id (str): The external identifier of the file server.
        replication_policy_ext_id (str): The external identifier of the VDI
            sync replication policy.
        ext_id (str): The external identifier of the VDI synchronization
            user session.
    return:
        info (object): VDI user session info wrapper containing ``.data``
            (VdiUserSession model) and the raw ETag headers.
    """
    try:
        return api_instance.get_vdi_user_session_by_id(
            fileServerExtId=file_server_ext_id,
            replicationPolicyExtId=replication_policy_ext_id,
            extId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VDI user session info using ext_id",
        )
