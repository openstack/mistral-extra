#  Copyright 2020 - Nokia Corporation
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

OPENSTACK_ACTIONS_GROUP = 'openstack_actions'

CONF = cfg.CONF

CONF.register_opts(openstack_actions_opts, group=OPENSTACK_ACTIONS_GROUP)
CONF.register_opt(os_actions_mapping_path)
