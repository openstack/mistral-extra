#!/usr/bin/env python
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

# TODO(rakhmerov): remove "mock" dependency later
import mock
from mistralclient.api import client as cl


MISTRAL_URL = "http://localhost:8989/v1"
WORKBOOK_NAME = "vm_job_workbook"
WORKBOOK_DEFINITION_FILE_NAME = "run_vm_job.yaml"
CONTEXT = {
    'image_id': '123'  # TODO(rakhmerov): needs to be calculated?
}

cl.Client.authenticate = mock.MagicMock(return_value=(MISTRAL_URL,
                                                      "", "", ""))
CLIENT = cl.Client(mistral_url=MISTRAL_URL, project_name="mistral_demo")


def create_workbook(wb_name):
    """Create a workbook with the given name if it doesn't exist."""
    wb = None

    for item in CLIENT.workbooks.list():
        if item.name == wb_name:
            wb = item
            break

    if not wb:
        wb = CLIENT.workbooks.create(wb_name,
                                     description="My test workbook",
                                     tags=["test"])
        print "Created workbook: %s" % wb
    else:
        print "Workbook already exists: %s" % wb


def upload_workbook_definition(wb_name, file_name):
    """Upload a workbook definition from the given file name."""
    with open(file_name) as definition_file:
        definition = definition_file.read()

    CLIENT.workbooks.upload_definition(wb_name, definition)

    print "\nUploaded workbook:\n\"\n%s\"\n" % \
          CLIENT.workbooks.get_definition(wb_name)


def create_execution(wb_name, task_name, context):
    execution = CLIENT.executions.create(wb_name, task_name, context)

    print "Created execution: %s" % execution


def main():
    """Main script."""
    create_workbook(WORKBOOK_NAME)
    upload_workbook_definition(WORKBOOK_NAME, WORKBOOK_DEFINITION_FILE_NAME)
    create_execution(WORKBOOK_NAME, "runJob", CONTEXT)


if __name__ == '__main__':
    main()
