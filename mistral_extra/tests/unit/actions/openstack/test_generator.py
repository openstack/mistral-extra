#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import os
from unittest import mock

from oslo_config import fixture as config_fixture
from oslotest import base

from mistral_extra.actions import generator_factory
from mistral_extra.actions.openstack.action_generator import base as \
    generator_base
from mistral_extra.actions.openstack import actions
from mistral_extra import config

RELATIVE_TEST_MAPPING_PATH = "tests/resources/openstack/test_mapping.json"
ABSOLUTE_TEST_MAPPING_PATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__),
                 "../../../resources/openstack/test_mapping.json")
)

MODULE_MAPPING = {
    'nova': ('nova.servers_get', 'servers.get', actions.NovaAction),
    'glance': ('glance.images_list', 'images.list', actions.GlanceAction),
    'keystone': ('keystone.users_create', 'users.create',
                 actions.KeystoneAction),
    'heat': ('heat.stacks_list', 'stacks.list', actions.HeatAction),
    'neutron': ('neutron.show_network', 'show_network',
                actions.NeutronAction),
    'cinder': ('cinder.volumes_list', 'volumes.list', actions.CinderAction),
    'trove': ('trove.instances_list', 'instances.list', actions.TroveAction),
    'ironic': ('ironic.node_list', 'node.list', actions.IronicAction),
    'baremetal_introspection': ('baremetal_introspection.introspect',
                                'introspect',
                                actions.BaremetalIntrospectionAction),
    'swift': ('swift.head_account', 'head_account', actions.SwiftAction),
    'swiftservice': ('swiftservice.delete', 'delete',
                     actions.SwiftServiceAction),
    'zaqar': ('zaqar.queue_messages', 'queue_messages', actions.ZaqarAction),
    'mistral': ('mistral.workflows_get', 'workflows.get',
                actions.MistralAction),
    'designate': ('designate.quotas_list', 'quotas.list',
                  actions.DesignateAction),
    'manila': ('manila.shares_list', 'shares.list', actions.ManilaAction),
    'magnum': ('magnum.mservices_list', 'mservices.list',
               actions.MagnumAction),
    'aodh': ('aodh.alarm_list', 'alarm.list', actions.AodhAction),
    'gnocchi': ('gnocchi.metric_list', 'metric.list', actions.GnocchiAction),
    'zun': ('zun.containers_list', 'containers.list', actions.ZunAction),
}

PREPARE_INPUTS_CASES = [
    ('a,b,c', 'a, b, c, region=RegionOne'),
    ('a,b,c=1', 'a, b, region=RegionOne, c=1'),
    ('a,b,c=1,**kwargs', 'a, b, region=RegionOne, c=1, **kwargs'),
    ('**kwargs', 'region=RegionOne, **kwargs'),
    ('', 'region=RegionOne'),
]


class GeneratorTest(base.BaseTestCase):
    def setUp(self):
        super(GeneratorTest, self).setUp()
        self.conf = self.useFixture(config_fixture.Config(config.CONF))

    # These clients try to reach their service when instantiated.
    @mock.patch.object(actions.ZunAction, 'get_fake_client_method',
                       return_value=lambda x: None)
    @mock.patch.object(actions.BaremetalIntrospectionAction,
                       'get_fake_client_method', return_value=lambda x: None)
    def test_create_actions(self, *_):
        region_modules = config.CONF.openstack_actions.modules_support_region

        for generator_cls in generator_factory.all_generators():
            namespace = generator_cls.action_namespace
            action_name, method_name, action_cls = MODULE_MAPPING[namespace]
            by_name = {a['name']: a for a in generator_cls.create_actions()}

            action = by_name[action_name]

            self.assertTrue(issubclass(action['class'], action_cls))
            self.assertEqual(method_name, action['class'].client_method_name)

            if namespace in region_modules:
                self.assertIn('action_region', action['arg_list'])

    def test_get_mapping_from_relative_or_absolute_path(self):
        for path in (RELATIVE_TEST_MAPPING_PATH, ABSOLUTE_TEST_MAPPING_PATH):
            self.conf.config(openstack_actions_mapping_path=path)

            mapping = generator_base.get_mapping()

            self.assertEqual(
                {'servers_get': 'servers.get',
                 'servers_find': 'servers.find',
                 'volumes_delete_server_volume':
                     'volumes.delete_server_volume'},
                mapping['nova']
            )

    def test_prepare_action_inputs(self):
        for origin, expected in PREPARE_INPUTS_CASES:
            self.assertEqual(
                expected,
                generator_base.OpenStackActionGenerator.prepare_action_inputs(
                    origin, added=['region=RegionOne'])
            )
