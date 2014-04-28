Webhooks scheduling
===================

What does this example do?
--------------------------

It runs small web-server and exposes one URL - 0.0.0.0:8988/ (host and port by default)
We can make request to /<name>, where name is the task name which will run on the server.
Actually, the server doesn't do any work, just sleeps for a few seconds (for simulate long execution) and then sends to Mistral info about task result and state.

### Prerequisites
For this Mistral example an OpenStack installation is optional.

In case of running the example without OpenStack server side authentication
based on Keystone must be disabled by setting configuration option "auth_enable"
under group "pecan" to False like the following:
```
[pecan]
auth_enable = False
```

### Running the example
From the root folder ("mistral-extra" by default) run the following shell command:<br><br>
```
tox -evenv -- python examples/webhooks/cmd/api.py -v
```
