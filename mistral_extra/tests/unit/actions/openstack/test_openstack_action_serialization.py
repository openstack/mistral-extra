# Copyright 2020 Nokia Software.
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

from oslotest import base


class OpenStackActionSerializationTest(base.BaseTestCase):
    @mock.patch.object(actions.NovaAction, '_get_client')
    def test_nova_action_serialization(self, mocked):
        mock_ctx = mock.Mock()

        method_name = "servers.get"

        # Create a dynamic action class.
        action_class = type(
            str(method_name),
            (actions.NovaAction,),
            {'client_method_name': method_name}
        )

        params = {'server': '1234-abcd'}

        # Just in case let's just make sure the action is functioning.
        action = action_class(**params)

        action.run(mock_ctx)

        self.assertTrue(mocked().servers.get.called)

        mocked().servers.get.assert_called_once_with(server="1234-abcd")

        # Now let's serialize the action.
        serializer = actions_base.OpenStackActionSerializer()

        serialized_action = serializer.serialize(action)

        self.assertIsNotNone(serialized_action)

        deserialized_action = serializer.deserialize(serialized_action)

        # Make sure that the action class is dynamic and it's still
        # functioning.
        self.assertNotEqual(actions.NovaAction, type(deserialized_action))

        deserialized_action.run(mock_ctx)

        self.assertTrue(mocked().servers.get.called)

        mocked().servers.get.assert_called_with(server="1234-abcd")

        self.assertEqual(2, mocked().servers.get.call_count)
