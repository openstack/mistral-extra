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

1. Preparing

  1. Create an image of virtual machine
  2. Make sure that VM has SSH server in running state
  3. Make sure that VM has password access via SSH
  4. Install packages (example for Debian/Ubuntu based systems)

          sudo apt-get install python-dev
          sudo apt-get install python-pip
          sudo pip install flask

  5. Put *web_app.py* file into user's home directory. To check if it works, type

          python ~/web_app.py

     This should run a small server on 5000 port.

  6. Save image

2. Make sure that python-mistralclient have been installed. If not, install it:

       git clone https://github.com/stackforge/python-mistralclient.git
       cd  python-mistralclient
       python setup.py install

3. Make sure that Mistral API and at least one Mistral-executor are up and running
4. Create workbook and upload the definition

       mistral workbook-create myWorkbook description tag1,tag2 <path to run_vm_job.yaml>

5. Create context file (simple json, which contains needed by workflow properties)

       {
         "server_name": "mistral-vm",
         "nova_url": "http://172.16.80.100:8774/v2",
         "image_id": "[copy from horizon or nova cli client]",
         "flavor_id": "1",
         "ssh_username": "[VM username]",
         "ssh_password": "[VM password]",
         "smtp_server": "[address to smtp server]",
         "from_email": "[email address]",
         "smtp_password": "[email password]",
         "admin_email": "[address the message should be sent to]",
       }

6. Start execution

       mistral execution-create myWorkbook createVM <path-to-the-context-file>
