# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_replication_job(module, api_instance, ext_id):
    """
    Fetch a single replication job by external ID via the
    `ReplicationJobsApi.get_replication_job_by_id` method.

    Args:
        module (AnsibleModule): The Ansible module instance.
        api_instance: `ReplicationJobsApi` instance.
        ext_id (str): The external ID of the replication job.

    Returns:
        object: SDK model of the replication job.
    """
    try:
        resp = api_instance.get_replication_job_by_id(extId=ext_id)
    except Exception as exc:
        raise_api_exception(
            module=module,
            exception=exc,
            msg="Api Exception raised while fetching replication job info using ext_id: {0}".format(
                ext_id
            ),
        )
        return None
    return resp.data
