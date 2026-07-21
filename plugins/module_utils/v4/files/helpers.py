# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_replication_job(module, api_instance, ext_id):
    """
    Fetch a single Nutanix Files Smart DR ReplicationJob by external ID.

    Args:
        module (AnsibleModule): the calling Ansible module (used only to
            report a descriptive failure via ``raise_api_exception``).
        api_instance (ntnx_files_py_client.ReplicationJobsApi): SDK receiver
            returned by ``get_replication_jobs_api_instance``.
        ext_id (str): the external identifier of the replication job to fetch.

    Returns:
        ntnx_files_py_client.ReplicationJob: the SDK model with the job
        metadata, progress counters, statuses, and mount target references.
    """
    try:
        return api_instance.get_replication_job_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching replication job info using ext_id",
        )
