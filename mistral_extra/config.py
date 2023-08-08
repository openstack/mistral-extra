#  Copyright 2020 - Nokia Corporation
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

import os

from oslo_config import cfg

os_actions_mapping_path = cfg.StrOpt(
    'openstack_actions_mapping_path',
    short='m',
    metavar='MAPPING_PATH',
    default='actions/openstack/mapping.json',
    help='Path to openstack action mapping json file.'
         'It could be relative to mistral package '
         'directory or absolute.'
)

openstack_actions_opts = [
    cfg.StrOpt(
        'os-actions-endpoint-type',
        default=os.environ.get('OS_ACTIONS_ENDPOINT_TYPE', 'public'),
        choices=['public', 'admin', 'internal'],
        deprecated_group='DEFAULT',
        help='Type of endpoint in identity service catalog to use for'
             ' communication with OpenStack services.'
    ),
    cfg.ListOpt(
        'modules-support-region',
        default=['nova', 'glance', 'heat', 'neutron', 'cinder',
                 'trove', 'ironic', 'designate', 'murano', 'tacker', 'senlin',
                 'aodh', 'gnocchi'],
        help='List of module names that support region in actions.'
    ),
    cfg.StrOpt(
        'default_region',
        help='Default region name for openstack actions supporting region.'
    ),
]

monitoring_opts = [
    cfg.BoolOpt(
        'enabled',
        default=False,
        help=('Parameter for monitoring-mode.')
    ),
    cfg.IntOpt(
        'metric_collection_interval',
        min=1,
        default=30,
        help=('Metric collection interval')
    )
]

recovery_job_opts = [
    cfg.BoolOpt(
        'enabled',
        default=True,
        help=('Parameter for enabling recovery job.')
    ),
    cfg.IntOpt(
        'recovery_interval',
        default=30,
        min=1,
        help=('Recovery interval')
    ),
    cfg.IntOpt(
        'hang_interval',
        default=600,
        min=1,
        help=('Timeout for scheduled calls to be in processing state')
    ),
    cfg.IntOpt(
        'idle_task_timeout',
        default=120,
        min=1,
        help=('Timeout for IDLE tasks to send run_task call again')
    ),
    cfg.IntOpt(
        'waiting_task_timeout',
        default=600,
        min=1,
        help=('Timeout for WAITING tasks to refresh its state again')
    ),
    cfg.IntOpt(
        'expired_subwf_task_timeout',
        default=600,
        min=1,
        help=('Timeout for subwf tasks without created subworkflow')
    ),
    cfg.IntOpt(
        'stucked_subwf_task_timeout',
        default=600,
        min=1,
        help=('Timeout for subwf tasks with completed subworkflow')
    )
]

OPENSTACK_ACTIONS_GROUP = 'openstack_actions'
MONITORING_GROUP = 'monitoring'
RECOVERY_JOB_GROUP = 'recovery_job'
CONF = cfg.CONF

CONF.register_opts(openstack_actions_opts, group=OPENSTACK_ACTIONS_GROUP)
CONF.register_opt(os_actions_mapping_path)
CONF.register_opts(monitoring_opts, group=MONITORING_GROUP)
CONF.register_opts(recovery_job_opts, group=RECOVERY_JOB_GROUP)
