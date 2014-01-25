Webhooks scheduling
===================

### Prerequisites
For this Mistral example an OpenStack installation is optional.

In case of running the example without OpenStack server side authentication
based on Keystone must be disabled by setting configuration option "auth_enable"
under group "pecan" to False like the following:

[pecan] <br>
auth_enable = False <br>


### Running the example
From the root folder ("mistral-extra" by default) run the following shell command:<br><br>
*tox -evenv -- python examples/webhooks/cmd/api.py --config-file path_to_config*
