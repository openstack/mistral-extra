#  Copyright 2023 - NetCracker Technology Corp.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from mistral.db.v2 import api as db_api
from mistral.workflow import states
from mistral_extra.monitoring import base

from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

TASK_STATES = [
    states.IDLE,
    states.WAITING,
    states.RUNNING,
    states.RUNNING_DELAYED,
    states.PAUSED,
    states.SUCCESS,
    states.CANCELLED,
    states.ERROR,
]

WORKFLOW_STATES = [
    states.RUNNING,
    states.PAUSED,
    states.SUCCESS,
    states.CANCELLED,
    states.ERROR,
]

ACTION_STATES = [
    states.RUNNING,
    states.PAUSED,
    states.SUCCESS,
    states.CANCELLED,
    states.ERROR
]

DC_TARGET_METHODS = [
    'mistral.engine.task_handler._refresh_task_state',
    'mistral.engine.task_handler._scheduled_on_action_complete',
    'mistral.engine.task_handler._scheduled_on_action_update',
    'mistral.engine.workflow_handler._check_and_complete',
    'mistral.engine.policies._continue_task',
    'mistral.engine.policies._complete_task',
    'mistral.engine.policies._fail_task_if_incomplete',
    'mistral.services.maintenance._pause_executions',
    'mistral.services.maintenance._resume_executions',
]


class MistralMetricCollector(base.MetricCollector):
    _metrics_data = []

    def collect(self):
        with db_api.transaction():
            self._update_action_count()
            self._update_task_count()
            self._update_workflow_count()
            self._update_delayed_call_count()

        return self._metrics_data

    def _update_action_count(self):
        counts = dict(db_api.get_action_execution_count_by_state())
        action_count_tags = {
            "name": "mistral_action_count",
            "description": "Count of action by state",
            "labels": ['namespace', 'state']
        }

        for state in ACTION_STATES:
            if state not in counts:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state).lower(), "value": 0},
                    tags=action_count_tags
                )
            else:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state).lower(),
                            "value": counts[state]},
                    tags=action_count_tags
                )

    def _update_task_count(self):
        counts = dict(db_api.get_task_execution_count_by_state())
        task_count_tags = {
            "name": "mistral_task_count",
            "description": "Count of tasks by state",
            "labels": ['namespace', 'state']
        }

        for state in TASK_STATES:
            if state not in counts:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state), "value": 0},
                    tags=task_count_tags
                )
            else:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state),
                            "value": counts[state]},
                    tags=task_count_tags
                )

    def _update_workflow_count(self):
        counts = dict(db_api.get_workflow_execution_count_by_state())
        workflow_count_tags = {
            "name": "mistral_workflow_count",
            "description": "Count of workflows by state",
            "labels": ['namespace', 'state']
        }

        for state in WORKFLOW_STATES:
            if state not in counts:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state), "value": 0},
                    tags=workflow_count_tags
                )
            else:
                base.add_metric(
                    self._metrics_data,
                    'mistral_entities',
                    fields={"state": str(state),
                            "value": counts[state]},
                    tags=workflow_count_tags
                )

    def _update_delayed_call_count(self):
        counts = dict(db_api.get_delayed_calls_count_by_target())
        delayed_calls_tags = {
            "name": "mistral_delayed_calls_count",
            "description": "Count of delayed calls by target method",
            "labels": ['namespace', 'target']
        }

        for target in DC_TARGET_METHODS:
            if target not in counts:
                base.add_metric(
                    self._metrics_data,
                    "mistral_entities",
                    fields={"target": str(target).lower(), "value": 0},
                    tags=delayed_calls_tags
                )
            else:
                base.add_metric(
                    self._metrics_data,
                    "mistral_entities",
                    fields={"target": str(target).lower(),
                            "value": counts[target]},
                    tags=delayed_calls_tags
                )
