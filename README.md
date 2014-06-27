Mistral Extras
==============

Contains example applications and additional tools for Mistral.

Currently, there are three examples:

#### Create VM

Connects to OpenStack Nova and creates a VM with image and flavor id provided.
See `examples/create_vm/README.md` for more.

#### Run VM job

Spins up a VM, deploys web server, sends request, reports by email if an error occurred.
See `examples/vm_job/README.md` for more.

#### Webhooks scheduling

Starts local webserver and then assess it periodically using HTTP action.
See `examples/webhooks/README.md` for more.
