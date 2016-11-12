=======================
Cloning virtual machine
=======================

Workflow ``clone_vm`` defines the process of creating a new VM based on
existing VM which was created using bootable volume (and may have other
additional volumes). It's also a good example of using sub-workflows in one
workflow.

To run the example:

1. Create sub-workflows ``clone_volume.yaml`` and
   ``boot_vm_from_volume.yaml``::

        mistral workflow-create clone_volume.yaml
        mistral workflow-create boot_vm_from_volume.yaml

2. Create workflow ``clone_vm.yaml``::

        mistral workflow-create clone_vm.yaml

3. Create ``input.json`` file containing workflow input parameters as follows::

        {
          "vm_name": "new_vm",
          "flavor_ref": "1",
          "source_root_vol_id": "1969299a-4c45-4900-bfe0-5ac65c1f2211",
          "root_vol_name": "new_root_vol",
          "root_vol_size": 1,
          "additional_volumes": [
            {
              "vol_name": "new_user_vol_1"，
              "vol_size": 1,
              "source_vol_id": "94391f69-a2f7-4406-b602-86e0b421d519"
            },
            {
              "vol_name": "new_user_vol_2"，
              "vol_size": 1,
              "source_vol_id": "262b37ab-86f1-4be5-ada2-645898400584"
            }
          ]
        }

5. Start workflow::

        mistral execution-create clone_vm input.json

6. Get execution status by using execution id from the previous command
   output::

        mistral execution-get <execution_id>

7. Make sure that a virtual machine with a bootable volume and two additional
   volumes has been created successfully. It can be done by opening Horizon UI
   or using Nova client (python-novaclient).
