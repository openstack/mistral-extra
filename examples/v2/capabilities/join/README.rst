=============================================
"join" control example (based on v2 API/DSL)
=============================================

Workflow ``create_vm_with_volume`` demonstrates usage of ``join`` workflow control
to synchronize multiple workflow routes. Specifically, it creates a virtual
machine and Cinder volume in parallel, waits till their completion using ``join``
and attaches the volume to the newly created virtual machine.

Note: Unlike some other examples this example doesn't use workbook concept.
File ``create_vm_with_volume.yaml`` contains a workflow definition in the first place
so in order to load the workflow "mistral workflow-create" CLI command must be
used (not "mistral workbook-create").

To run the example:

1. Load workflow ``create_vm_with_volume.yaml``::

        mistral workflow-create create_vm_with_volume.yaml

2. Create ``input.json`` file containing workflow input parameters as follows::

        {
            "server_name": "mistral_test_vm",
            "image_id": "aaacd887-5afa-4cb7-a33d-1ef0b72d21c4",
            "flavor_id": "2",
            "ssh_username": "ubuntu",
            "ssh_password": "my_pass",
            "volume_name": "mistral_test_volume"
        }

3. Start workflow::

        mistral execution-create create_vm_with_volume input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

5. Make sure that a virtual machine and a volume have been created.
   It can be done by opening Horizon UI or using Nova client (python-novaclient).
