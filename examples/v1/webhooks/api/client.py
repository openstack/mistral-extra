# -*- coding: utf-8 -*-
#
# Copyright 2013 - Mirantis, Inc.
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

import pkg_resources as pkg

from mistralclient.api import client
from mistralclient.openstack.common.cliutils import env

from examples.v1.webhooks import version

from oslo.config import cfg


MISTRAL_URL = env('OS_MISTRAL_URL', default=cfg.CONF.client.mistral_url)
if MISTRAL_URL.find("v2") != -1:
    raise RuntimeError("Can not run this example, please provide the correct"
                       "Mistral v1 URL (default is %s)"
                       % cfg.CONF.client.mistral_url)


CLIENT = client.client(
    mistral_url=MISTRAL_URL,
    auth_url=env('OS_AUTH_URL', default=cfg.CONF.client.auth_url),
    username=env('OS_USERNAME', default=cfg.CONF.client.username),
    api_key=env('OS_PASSWORD', default=cfg.CONF.client.password),
    project_name=env('OS_TENANT_NAME', default=cfg.CONF.client.tenant_name)
)


WB_NAME = "myWorkbook"
TASK = "execute_backup"


def upload_workbook():
    try:
        CLIENT.workbooks.get(WB_NAME)
    except:
        CLIENT.workbooks.create(WB_NAME,
                                description="My test workbook",
                                tags=["test"])
    print("Uploading workbook definition...\n")

    definition = get_workbook_definition()
    CLIENT.workbooks.upload_definition(WB_NAME, definition)

    print definition
    print("\nUploaded.")


def get_workbook_definition():
    return open(pkg.resource_filename(version.version_info.package,
                                      "demo.yaml")).read()


def start_execution():
    import threading
    t = threading.Thread(target=CLIENT.executions.create,
                         kwargs={'workbook_name': WB_NAME,
                                 'task': TASK})
    t.start()
    return "accepted"
