# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslotest import base

from mistral_extra import config


class ListOptsTest(base.BaseTestCase):

    def test_os_actions_endpoint_type_listed(self):
        opts = dict(config.list_opts())[config.OPENSTACK_ACTIONS_GROUP]
        self.assertIn('os_actions_endpoint_type', [o.dest for o in opts])
