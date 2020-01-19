# Copyright 2017 - Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

from oslo_log import log as logging
from oslotest import base


LOG = logging.getLogger(__name__)


class BaseTest(base.BaseTestCase):
    def setUp(self):
        super(BaseTest, self).setUp()

    def _assert_single_item(self, items, **props):
        return self._assert_multiple_items(items, 1, **props)[0]

    def _assert_multiple_items(self, items, count, **props):
        def _matches(item, **props):
            for prop_name, prop_val in props.items():
                v = item[prop_name] if isinstance(
                    item, dict) else getattr(item, prop_name)

                if v != prop_val:
                    return False

            return True

        filtered_items = list(
            [item for item in items if _matches(item, **props)]
        )

        found = len(filtered_items)

        if found != count:
            LOG.info("[failed test ctx] items=%s, expected_props=%s", str(
                items), props)
            self.fail("Wrong number of items found [props=%s, "
                      "expected=%s, found=%s]" % (props, count, found))

        return filtered_items
