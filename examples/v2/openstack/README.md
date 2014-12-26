OpenStack actions examples (based on v2 API/DSL)
================================================

These examples demonstrate how to use OpenStack Mistral actions in Mistral
workflows.

Glance actions
--------------

glance_actions.yaml file contains workbook "glance_action" with one workflow
"get_first_glance_image". The purpose of this workflow is to interact with
OpenStack Glance service and obtain information about first encountered
Glance image.

To run the example:

1. Load workbook from glance_actions.yaml:

        mistral workbook-create glance_actions.yaml

1. Start workflow:

        mistral execution-create glance_actions.get_first_glance_image

1. Using execution id from the previous step wait for completion (workflow SUCCESS state):

        mistral execution-get <execution_id>

1. See the result of the workflow (image info):

        mistral execution-get-output <execution_id>

Keystone actions
----------------

Similar to the previous example (Glance actions) keystone_actions.yaml file
contains workbook "keystone_actions" with one workflow "get_first_keystone_project".
The purpose of this workflow is to interact with OpenStack Keystone service and
obtain information about first encountered Keystone project.

To run the example:

1. Load workbook from keystone_actions.yaml:

        mistral workbook-create keystone_actions.yaml

1. Start workflow:

        mistral execution-create keystone_actions.get_first_keystone_project

1. Using execution id from the previous step wait for completion (workflow SUCCESS state):

        mistral execution-get <execution_id>

1. See the result of the workflow (Keystone project info):

        mistral execution-get-output <execution_id>


Nova actions
------------

Workflow "create_vm" located in workbook file "nova_actions" demonstrates
how to create a new virtual machine with Nova service and wait till it is
in active state using "retry" task policy. Unlike other examples this workflow
takes input parameters.


To run the example:

1. Load workbook from nova_actions.yaml:

        mistral workbook-create nova_actions.yaml

1. Create input.json file containing workflow input parameters as follows:

        {
            "vm_name": "my_test_virtual_machine",
            "image_ref": "5486c382-fce3-4bde-abb3-51273a98c006",
            "flavor_ref": "2"
        }

1. Start workflow:

        mistral execution-create nova_actions.create_vm input.json

1. Using execution id from the previous step wait for completion (workflow SUCCESS state):

        mistral execution-get <execution_id>

1. See the result of the workflow (virtual machine identifier):

        mistral execution-get-output <execution_id>
