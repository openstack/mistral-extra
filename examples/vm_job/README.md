Run VM job example
==================

Run VM job example is created to demonstrate Mistral project features:
It is needed for spinning up a VM and use it to do some useful work given calculator as an example.

What this example does
--------------------

 1. Creates a VM
 2. Waits till it is up and running
 3. Runs small web server on VM
 4. Sends request to the server
 5. If an error occurred, it sends a email to admin with error message

How to run
----------

 - Preparing
   - Create your own image of virtual machine
   - Make sure that VM has SSH server in running state
   - Make sure that VM has password access via SSH
   - Install packages (example for Debian/Ubuntu based systems)

     ```
     sudo apt-get install python-dev
     sudo apt-get install python-pip
     sudo pip install flask
     ```

   - Put *web_app.py* file in your home user directory
      > To check if it works, please type
      ```python ~/web_app.py```
      > (this should run a small server on 5000 port)
   - Save image

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
   mistral workbook-create myWorkbook description tag1,tag2 <path to run_vm_job.yaml>
   ```

 - Create context file (simple json, which contains needed by workflow properties)

   ```
   {
     "server_name": "name_of_your_VM",
     "nova_url": "url_to_nova_service",
     "image_id": "id_of_your_image",
     "flavor_id": "id_of_flavor",
     "ssh_username": "your_VM_username",
     "ssh_password": "your_VM_password",
     "smtp_server": "address_to_smtp_server",
     "from_email": "your_email_address",
     "smtp_password": "password_of_your_email",
     "admin_email": "address_on_which_you_wish_to_send_messages",
   }
   ```

 - Start execution
   ```
   mistral execution-create myWorkbook createVM <path-to-the-context-file>
   ```
