# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from ..prism.recovery_plans import get_recovery_plan_uuid
from .prism import Prism

__metaclass__ = type


class RecoveryPlanJob(Prism):
    def __init__(self, module):
        resource_type = "/recovery_plan_jobs"
        super(RecoveryPlanJob, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "recovery_plan": self._build_spec_recovery_plan,
            "failed_site": self._build_spec_failed_site,
            "recovery_site": self._build_spec_recovery_site,
            "action": self._build_spec_action,
            "recovery_reference_time": self._build_spec_recovery_reference_time,
            "ignore_validation_failures": self._build_spec_ignore_validation_failures,
        }
        self.action_endpoints = {"CLEANUP": "cleanup"}

    def perform_action_on_existing_job(self, job_uuid, action, spec={}):
        endpoint = "{0}/{1}".format(job_uuid, self.action_endpoints[action])
        return self.create(data=spec, endpoint=endpoint)

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "recovery_plan_job"},
                "spec": {
                    "resources": {
                        "execution_parameters": {
                            "failed_availability_zone_list": [],
                            "recovery_availability_zone_list": [],
                            "action_type": None,
                        },
                        "recovery_plan_reference": {},
                    },
                    "name": None,
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_recovery_plan(self, payload, recovery_plan):
        uuid, err = get_recovery_plan_uuid(recovery_plan, self.module)
        if err:
            return err
        payload["spec"]["resources"]["recovery_plan_reference"] = {
            "uuid": uuid,
            "kind": "recovery_plan",
        }
        return payload, None

    def _build_spec_failed_site(self, payload, failed_site):
        az_spec = {"availability_zone_url": failed_site["url"]}
        if failed_site.get("cluster"):
            az_spec["cluster_reference_list"] = [{"uuid": failed_site["cluster"]}]
        payload["spec"]["resources"]["execution_parameters"][
            "failed_availability_zone_list"
        ] = [az_spec]
        return payload, None

    def _build_spec_recovery_site(self, payload, recovery_site):
        az_spec = {"availability_zone_url": recovery_site["url"]}
        if recovery_site.get("cluster"):
            az_spec["cluster_reference_list"] = [{"uuid": recovery_site["cluster"]}]
        payload["spec"]["resources"]["execution_parameters"][
            "recovery_availability_zone_list"
        ] = [az_spec]
        return payload, None

    def _build_spec_action(self, payload, action):
        payload["spec"]["resources"]["execution_parameters"]["action_type"] = action
        return payload, None

    def _build_spec_recovery_reference_time(self, payload, recovery_reference_time):
        payload["spec"]["resources"]["execution_parameters"][
            "recovery_reference_time"
        ] = recovery_reference_time
        return payload, None

    def _build_spec_ignore_validation_failures(
        self, payload, ignore_validation_failures
    ):
        payload["spec"]["resources"]["execution_parameters"][
            "should_continue_on_validation_failure"
        ] = ignore_validation_failures
        return payload, None
