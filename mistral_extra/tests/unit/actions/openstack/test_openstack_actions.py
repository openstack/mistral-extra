# Copyright 2014 - Mirantis, Inc.
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

from unittest import mock

from mistral_extra.actions.openstack import actions
from mistral_extra.actions.openstack import base as actions_base
from oslo_config import cfg
from oslo_config import fixture as config_fixture
from oslo_utils import importutils
from oslotest import base

CONF = cfg.CONF
CONF.register_opt(cfg.BoolOpt('auth_enable'), group='pecan')
CONF.register_opt(cfg.HostAddressOpt('host'), group='api')
CONF.register_opt(cfg.PortOpt('port'), group='api')


def _action(base_cls, method_name, **params):
    cls = type(method_name, (base_cls,), {'client_method_name': method_name})
    return cls(**params)


class OpenStackActionTest(base.BaseTestCase):
    @mock.patch.object(actions.NovaAction, '_get_client')
    def test_run_calls_nested_client_method(self, mocked):
        _action(actions.NovaAction, 'servers.get', server='1234').run(
            mock.Mock())

        mocked().servers.get.assert_called_once_with(server='1234')

    @mock.patch.object(actions.ZaqarAction, '_get_client')
    def test_zaqar_run_dispatches_to_static_method(self, mocked):
        _action(actions.ZaqarAction, 'queue_messages', queue_name='foo').run(
            mock.Mock())

        mocked().queue.assert_called_once_with('foo')
        mocked().queue().messages.assert_called_once_with()

    def test_serialization_round_trip_keeps_dynamic_class(self):
        action = _action(actions.NovaAction, 'servers.get', server='1234')
        serializer = actions_base.OpenStackActionSerializer()

        restored = serializer.deserialize(serializer.serialize(action))

        self.assertIsInstance(restored, actions.NovaAction)
        self.assertIsNot(actions.NovaAction, type(restored))
        self.assertEqual('servers.get', restored.client_method_name)
        self.assertEqual({'server': '1234'}, restored._kwargs_for_run)


class MistralActionClientTest(base.BaseTestCase):
    def setUp(self):
        super(MistralActionClientTest, self).setUp()
        self.conf = self.useFixture(config_fixture.Config(CONF))

    @mock.patch.object(actions.MistralAction, 'get_session_and_auth')
    def test_uses_keystone_endpoint_when_auth_enabled(self, mocked):
        self.conf.config(auth_enable=True, group='pecan')
        mocked.return_value = {
            'auth': mock.Mock(endpoint='http://mistral.test:8989/v2'),
            'session': None,
        }

        client = actions.MistralAction()._get_client(mock.Mock())

        self.assertEqual('http://mistral.test:8989/v2',
                         client.workbooks.http_client.base_url)

    def test_uses_local_api_when_auth_disabled(self):
        self.conf.config(auth_enable=False, group='pecan')
        self.conf.config(host='10.0.0.1', port=8989, group='api')

        client = actions.MistralAction()._get_client(mock.Mock())

        self.assertEqual('http://10.0.0.1:8989/v2',
                         client.workbooks.http_client.base_url)


class TestImport(base.BaseTestCase):
    @mock.patch.object(importutils, 'try_import')
    def test_try_import_fails(self, mocked):
        mocked.side_effect = Exception('Exception when importing module')

        self.assertIsNone(actions._try_import('raiser'))
