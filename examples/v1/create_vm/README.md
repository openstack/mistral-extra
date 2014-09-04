Create VM example
==================

It demonstrates Mistral project features:
This example connects to OpenStack Nova and creates a VM with image and flavor id provided.

How to run
----------

1. Make sure that python-mistralclient have been installed. If not, install it:

        git clone https://github.com/stackforge/python-mistralclient.git
        cd python-mistralclient
        python setup.py install

2. Make sure that Mistral API and at least one Mistral-executor are up and running
3. Create workbook and upload the definition

        mistral workbook-create myWorkbook description tag1,tag2 <path to create_vm_example.yaml>

4. Create context file (simple json, which contains needed by workflow properties)

        {
          "server_name": "mistral-vm",
          "nova_url": "http://localhost:8774/v2",
          "image_id": "[copy from horizon or nova cli client]",
          "flavor_id": "1"
        }

5. Start execution

        mistral execution-create myWorkbook create-vm <path-to-the-context-file>
