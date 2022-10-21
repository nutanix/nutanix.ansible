#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_time_machines_info
short_description: info module for ndb time machines
version_added: 1.8.0-beta.1
description: 'Get tm info'
options:
      name:
        description:
            - time machine name
        type: str
      uuid:
        description:
            - time machine id
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era time machines
  ntnx_ndb_time_machines_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: tms

- name: get era time machines using it's name
  ntnx_ndb_time_machines_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: List time machines use id
  ntnx_ndb_time_machines_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of time mashine>"
  register: result
"""
RETURN = r"""
response:
  description: listing all time machines
  returned: always
  type: list
  sample:
    [
                {
                    "accessLevel": null,
                    "associatedClusters": null,
                    "category": "DB_GROUP_IMPLICIT",
                    "clone": false,
                    "clones": null,
                    "clustered": false,
                    "database": null,
                    "databaseId": "e4dsad7f-d643-43c5-8e11-83dasdabf16fa",
                    "dateCreated": "2022-10-17 12:50:50",
                    "dateModified": "2022-10-19 13:07:07",
                    "description": "Time Machine for instance 'PRAD_POSTGRESS'",
                    "eaStatus": "NOT_APPLICABLE",
                    "id": "b05dasd42-1b96-40ba-89ef-52e9das003",
                    "info": null,
                    "internal": false,
                    "metadata": {
                        "absoluteThresholdExhausted": false,
                        "authorizedDbservers": [
                            "eafdsaef-5e63-4e93-bfa5-bb79dsad3f3c"
                        ],
                        "autoHeal": true,
                        "autoHealLogCatchupCount": 0,
                        "autoHealRetryCount": 0,
                        "autoHealSnapshotCount": 0,
                        "autoSnapshotRetryInfo": null,
                        "capabilityResetTime": null,
                        "databasesFirstSnapshotInfo": null,
                        "deregisterInfo": null,
                        "dispatchOnboardingSnapshot": false,
                        "firstSnapshotCaptured": true,
                        "firstSnapshotDispatched": true,
                        "firstSnapshotRetryCount": 0,
                        "implicitResumeCount": 0,
                        "info": null,
                        "lastAutoSnapshotOperationId": "16dasd7-bf83-46b6-9386-55adsad103",
                        "lastAutoSnapshotTime": "2022-10-18 14:02:27",
                        "lastEaBreakdownTime": null,
                        "lastHealSnapshotOperation": null,
                        "lastHealSystemTriggered": false,
                        "lastHealTime": null,
                        "lastHealthAlertedTime": null,
                        "lastImplicitResumeTime": null,
                        "lastLogCatchupOperationId": null,
                        "lastLogCatchupSkipped": false,
                        "lastLogCatchupTime": null,
                        "lastNonExtraAutoSnapshotTime": "2022-10-18 14:02:27",
                        "lastPauseByForce": false,
                        "lastPauseReason": null,
                        "lastPauseTime": null,
                        "lastResumeTime": null,
                        "lastSnapshotOperationId": "16edsad7-bf83-46b6-9386-55dasd8103",
                        "lastSnapshotTime": "2022-10-18 14:02:23",
                        "lastSuccessfulLogCatchupOperationId": null,
                        "lastSuccessfulLogCatchupPostHealWithResetCapability": null,
                        "lastSuccessfulSnapshotOperationId": "16edsad7-bf83-46b6-9386-55ab1dsad103",
                        "logCatchupSuccessiveFailureCount": 0,
                        "onboardingSnapshotProperties": null,
                        "requiredSpace": 0.0,
                        "secureInfo": null,
                        "snapshotCapturedForTheDay": false,
                        "snapshotSuccessiveFailureCount": 0,
                        "stateBeforeRestore": null,
                        "storageLimitExhausted": false
                    },
                    "metric": null,
                    "name": "PRAD_POSTGRESS_TM_1",
                    "ownerId": "eac7dsaf-22fb-462b-9498-949796dsad73",
                    "properties": [
                        {
                            "description": null,
                            "name": "CLONE_COUNT",
                            "ref_id": "b05dsa42-1b96-40ba-89ef-52e9fdsa7003",
                            "secure": false,
                            "value": "1"
                        }
                    ],
                    "schedule": {
                        "continuousSchedule": {
                            "enabled": true,
                            "logBackupInterval": 30,
                            "snapshotsPerDay": 1
                        },
                        "dailySchedule": null,
                        "dateCreated": "2022-10-17 12:50:50.016262",
                        "dateModified": "2022-10-17 12:50:50.016262",
                        "description": "Schedule for Time Machine PRAD_POSTGRESS_TM_1",
                        "globalPolicy": false,
                        "id": "87ddsad76-66ac-44a7-b645-57cedasd441e",
                        "monthlySchedule": {
                            "dayOfMonth": 17,
                            "enabled": true
                        },
                        "name": "Schedule_PRAD_POSTGRESS_TM_1_2022-10-17 12:50:50",
                        "ownerId": "edasddbf-22fb-462b-9498-9497dsad1f73",
                        "quartelySchedule": {
                            "dayOfMonth": 17,
                            "enabled": true,
                            "startMonth": "JANUARY",
                            "startMonthValue": "JANUARY"
                        },
                        "referenceCount": 1,
                        "snapshotTimeOfDay": {
                            "extra": false,
                            "hours": 14,
                            "minutes": 0,
                            "seconds": 0
                        },
                        "startTime": null,
                        "systemPolicy": false,
                        "timeZone": null,
                        "uniqueName": "SCHEDULE_PRAD_POSTGRESS_TM_1_2022-10-17 12:50:50",
                        "weeklySchedule": {
                            "dayOfWeek": "MONDAY",
                            "dayOfWeekValue": "MONDAY",
                            "enabled": true
                        },
                        "yearlySchedule": {
                            "dayOfMonth": 31,
                            "enabled": false,
                            "month": "DECEMBER",
                            "monthValue": null
                        }
                    },
                    "scheduleId": "87dfdsad6-66ac-44a7-b645-57cedsad41e",
                    "scope": "LOCAL",
                    "sla": {
                        "continuousRetention": 0,
                        "currentActiveFrequency": "DAILY",
                        "dailyRetention": 7,
                        "dateCreated": "2022-04-08 16:21:51.591815",
                        "dateModified": "2022-04-08 16:21:51.591815",
                        "description": "Out of the box Brass SLA for Era Time Machines. All retentions except daily retention are disabled.",
                        "id": "4d9ddsad6d-b6f8-47f0-8015-9e69dsadd3cf4",
                        "monthlyRetention": 0,
                        "name": "DEFAULT_OOB_BRASS_SLA",
                        "ownerId": "era-internal-user-id",
                        "pitrEnabled": false,
                        "quarterlyRetention": 0,
                        "referenceCount": 1,
                        "systemSla": true,
                        "uniqueName": "DEFAULT_OOB_BRASS_SLA",
                        "weeklyRetention": 0,
                        "yearlyRetention": 0
                    },
                    "slaId": "4d9dsadd-b6f8-47f0-8015-9e69dasdd3cf4",
                    "slaUpdateInProgress": false,
                    "slaUpdateMetadata": null,
                    "sourceNxClusters": [
                        "d7dasdb99-5a9d-4da7-8e7d-c93dsad14de"
                    ],
                    "status": "READY",
                    "tags": [],
                    "type": "postgres_database"
                }
            ]

"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_tm(module, result):
    tm = TimeMachine(module)

    uuid = module.params.get("uuid")
    name = module.params.get("name")
    resp, err = tm.get_time_machine(uuid=uuid, name=name)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching time machine info", **result)
    result["response"] = resp


def get_tms(module, result):
    tm = TimeMachine(module)

    resp = tm.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_tm(module, result)
    else:
        get_tms(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
