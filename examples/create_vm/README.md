Create VM example
==================

It demonstrates Mistral project features:
This example connects to OpenStack Nova and creates a VM with image id and flavor id you provided.

How to run
----------

 - Make sure that you have installed python-mistralclient
   - if not, install it:

     ```
     git clone https://github.com/stackforge/python-mistralclient.git
     cd  python-mistralclient
     python setup.py install
     ```

 - Make sure that Mistral API and at least one Mistral-executor are up and running
 - Create workbook and upload the definition

   ```
   mistral workbook-create myWorkbook description tag1,tag2 <path to create_vm_example.yaml>
   ```

 - Create context file (simple json, which contains needed by workflow properties)
   
   ```
   {
     "server_name": "name_of_your_VM",
     "nova_url": "url_to_nova_service",
     "image_id": "id_of_your_image",
     "network_id": "your_network_id_for_associate_with_VM",
     "flavor_id": "id_of_flavor",
   }
   ```

 - Start execution

   ```
   mistral execution-create myWorkbook create-vm <path-to-the-context-file>
   ```