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

from mistral_lib import utils

PRE_INSTALLED_WF_PATH = 'resources/openstack/workflows'


def get_preinstalled_workflows():
    return utils.get_file_list(PRE_INSTALLED_WF_PATH, package='mistral_extra')
