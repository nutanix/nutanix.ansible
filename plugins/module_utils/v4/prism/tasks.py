# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..utils import strip_internal_attributes  # noqa: E40

__metaclass__ = type

import base64  # noqa: E40
import time  # noqa: E40
import traceback  # noqa: E40

PRISM_SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client  # noqa: E40
except ImportError:
    PRISM_SDK_IMP_ERROR = traceback.format_exc()


from ..constants import Tasks  # noqa: E40
from .pc_api_client import get_pc_api_client  # noqa: E40


def wait_for_completion(
    module,
    ext_id,
    task_service=None,
    polling_gap=2,
    raise_error=True,
    add_task_service=False,
):
    """
    Wait for a task to complete.
    Args:
        module: The Ansible module.
        ext_id: The external ID of the task.
        task_service: The service of the task.
        polling_gap: The time interval between polling.
        raise_error: Flag to raise an error if the task fails.
        add_task_service: Flag to add the task service to the external ID.
    Returns:
        Task data.
    """
    api_client = get_pc_api_client(module=module)
    tasks = ntnx_prism_py_client.TasksApi(api_client=api_client)

    # add encoded service prefix to create complete task external ID
    if add_task_service:
        if task_service:
            ext_id = base64.b64encode(task_service.encode()).decode() + ":" + ext_id
        else:
            ext_id = (
                base64.b64encode(Tasks.TASK_SERVICE.encode()).decode() + ":" + ext_id
            )

    status = ""

    timeout_time = None
    if module.params.get("timeout", None):
        timeout_time = time.time() + module.params.get("timeout")

    while status != "SUCCEEDED":
        task = tasks.get_task_by_id(ext_id).data
        # convert to dict to output as module output in case of errors
        resp = deepcopy(task)
        if not isinstance(resp, dict):
            resp = resp.to_dict()

        status = resp["status"]

        if not status:
            module.fail_json(
                msg="Unable to fetch task status",
                response=strip_internal_attributes(resp),
            )
        if status == "FAILED":
            if not raise_error:
                break
            module.fail_json(
                msg="Task Failed",
                response=strip_internal_attributes(resp),
            )
        time.sleep(polling_gap)
        if timeout_time:
            if time.time() > timeout_time:
                module.fail_json(
                    msg="Timeout Error: Task did not complete in time",
                    response=strip_internal_attributes(resp),
                )

    return task


def get_entity_ext_id_from_task(data, rel=None):
    """
    Get the external ID of an entity from a task.
    Args:
        data: The task data.
        rel: Entity type identified as 'namespace:module[:submodule]:entityType'
    Returns:
        The external ID of the entity, or None if not found.
    """
    entities_affected = getattr(data, "entities_affected", [])
    if not entities_affected:
        return None

    ext_id = None
    for entity in entities_affected:
        if rel:
            if entity.rel == rel:
                ext_id = entity.ext_id
                break
        else:
            ext_id = entity.ext_id
            break

    return ext_id


def get_ext_id_from_task_completion_details(data, name=None):
    """
    Get the external ID of an entity from a task info.
    Args:
        data(object): The task info object.
        name(str): Name of the entity.
    Returns:
        The external ID of the entity, or None if not found.
    """
    completion_details = getattr(data, "completion_details", [])
    if not completion_details:
        return None

    ext_id = None
    for entity in completion_details:
        if name:
            if entity.name == name:
                ext_id = entity.value
                break
        else:
            ext_id = entity.value
            break

    return ext_id


def wait_for_entity_ext_id_in_task(module, ext_id, rel, time_out=300):
    """
    Wait for an entity external ID in a task.
    Args:
        module: The Ansible module.
        ext_id: The external ID of the task.
        rel: Entity type identified as 'namespace:module[:submodule]:entityType'
    Returns:
        ext_id(str): The external ID of the entity.
        err(str): Error message.
    """
    data = wait_for_completion(module=module, ext_id=ext_id)
    err = None
    while time_out > 0:
        entity_ext_id = get_entity_ext_id_from_task(data=data, rel=rel)
        if entity_ext_id:
            return entity_ext_id, err
        time.sleep(2)
        time_out -= 2
        data = wait_for_completion(module=module, ext_id=ext_id)
    err = "Timeout Error: Timeout while waiting for ext_id of entity to come in task"
    return None, err
