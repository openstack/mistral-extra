================================================
OpenStack actions examples (based on v2 API/DSL)
================================================

These examples demonstrate how to use OpenStack Mistral actions in Mistral
workflows.

Glance actions
--------------

``glance_actions.yaml`` file contains workbook ``glance_action`` with one workflow
``get_first_glance_image``. The purpose of this workflow is to interact with
OpenStack Glance service and obtain information about first encountered
Glance image.

To run the example:

1. Load workbook from ``glance_actions.yaml``::

        mistral workbook-create glance_actions.yaml

2. Start workflow::

        mistral execution-create glance_actions.get_first_glance_image

3. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

4. See the result of the workflow (image info)::

        mistral execution-get-output <execution_id>

Keystone actions
----------------

Similar to the previous example (Glance actions) ``keystone_actions.yaml`` file
contains workbook ``keystone_actions`` with one workflow ``get_first_keystone_project``.
The purpose of this workflow is to interact with OpenStack Keystone service and
obtain information about first encountered Keystone project.

To run the example:

1. Load workbook from ``keystone_actions.yaml``::

        mistral workbook-create keystone_actions.yaml

2. Start workflow::

        mistral execution-create keystone_actions.get_first_keystone_project

3. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

4. See the result of the workflow (Keystone project info)::

        mistral execution-get-output <execution_id>


Nova actions
------------

Workflow ``create_vm`` located in workbook file ``nova_actions.yaml`` demonstrates
how to create a new virtual machine with Nova service and wait till it is
in active state using "retry" task policy. Unlike other examples this workflow
takes input parameters.


To run the example:

1. Load workbook from ``nova_actions.yaml``::

        mistral workbook-create nova_actions.yaml

2. Create ``input.json`` file containing workflow input parameters as follows::

        {
            "vm_name": "my_test_virtual_machine",
            "image_ref": "5486c382-fce3-4bde-abb3-51273a98c006",
            "flavor_ref": "2"
        }

3. Start workflow::

        mistral execution-create nova_actions.create_vm input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

5. See the result of the workflow (virtual machine identifier)::

        mistral execution-get-output <execution_id>

Update kernel
-------------

Workflow ``update_kernel`` located in file ``update_kernel.yaml`` demonstrates
how to do some job on each VM in a tenant, particularly, how to upgrade VM kernel.
Workflow can take either an array of **vm_ids** or all VMs in a tenant. Note that
this workflow requires gateway VM with assigned floating IP which should be able to
access to guest network in a tenant.

**NOTE**: The workflow uses *std.ssh_proxied* action which requires existing private key
file at executor host in **<home-user-directory>/.ssh/<private_key_filename>**
**NOTE**: This upgrade kernel command works only for Ubuntu.

To run the example:

1. Load workflow from ``update_kernel.yaml``::

        mistral workflow-create update_kernel.yaml

2. Create ``input.json`` file containing workflow input parameters as follows::

        {
            "private_key_filename": "my_key.pem",
            "gateway_host": "172.16.111.16",
        }

or::

        {
            "private_key_filename": "my_key.pem",
            "gateway_host": "172.16.111.16",
            "vm_ids": ["5486c382-fce3-4bde-abb3-51273a98c006", "7485f786-bcd1-8def-fed7-25637a89e600"]
        }

3. Start workflow::

        mistral execution-create upgrade_kernel_on_vms input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>


Crawl specific data
-------------------

Workflow ``crawl_specific_data`` located in file ``crawl_specific_data.yaml`` demonstrates
how to do some job on each VM in a tenant, particularly, how to get specific data from VMs and
send this data via email. Workflow can take either an array of **vm_ids** or all VMs
in a tenant. Note that this workflow requires gateway VM with assigned floating
IP which should be able to access to guest network in a tenant.

**NOTE**: The workflow uses *std.ssh_proxied* action which requires existing private key
file at executor host in **<home-user-directory>/.ssh/<private_key_filename>**
**NOTE**: This upgrade kernel command works only for Ubuntu.

To run the example:

1. Load workflow from ``crawl_specific_data.yaml``::

        mistral workflow-create crawl_specific_data.yaml

2. Create ``input.json`` file containing workflow input parameters as follows::

        {
            "private_key_filename": "my_key.pem",
            "gateway_host": "172.16.111.16",
        }

or::

        {
            "private_key_filename": "my_key.pem",
            "gateway_host": "172.16.111.16",
            "vm_ids": ["5486c382-fce3-4bde-abb3-51273a98c006", "7485f786-bcd1-8def-fed7-25637a89e600"]
        }

or, if you want to see email report, provide also an email info::

        {
            "private_key_filename": "my_key.pem",
            "gateway_host": "172.16.111.16",
            "from_email": "my_email@example.com",
            "to_email": "admin_email@example.com",
            "smtp_server": "smtp.gmail.com:587",
            "smtp_password": "secret"
        }

3. Start workflow::

        mistral execution-create crawl_data_from_vms input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

