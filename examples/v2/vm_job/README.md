VM job example (based on v2 API/DSL)
========================================

'VM job example' is created to demonstrate Mistral project features:
It spins up a VM and uses it to do some useful work. Particularly, created vm
is used to deploy a simple web application on it which works a as a calculator
returning over HTTP results of sum operations.

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

       mistral workbook-create myWorkbook tag1,tag2 <path to run_vm_job.yaml>

5. Create workflow input file (simple json)

       {
         "server_name": "mistral-vm",
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

       mistral execution-create myWorkbook.run_vm_job <path-to-input-file>