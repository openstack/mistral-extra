============================================================
Multiple services registration example (based on v2 API/DSL)
============================================================

The example is created to demonstrate how Mistral can be used to interact
with multiple third party service's API. This specific example
works with Vyatta Firewall service and Zabbix monitoring service. It registers
a newly created VM in Zabbix service and Vyatta Firewall. It
requires two created workflows - Zabbix machine registration and Vyatta
Firewall. They can be found in corresponding directories - ``zabbix`` and
``vyatta``.

How to run
----------

1. Load workbook from multiple_services_registration.yaml::

    mistral workbook-create multiple_services_registration.yaml

2. Make sure you have created Zabbix and Vyatta workflows::

    mistral workbook-update vyatta_firewall.yaml
    mistral workbook-update zabbix_machine_registration.yaml

3. Create ``input.json`` file containing workflow input::

    {
      "server_name": [Name of the new instance],
      "server_port": [Port to open],
      "image_id": [image id from Glance service],
      "flavor_id": [flavor id - type of instance hardware],
      "ssh_username": [VM username],
      "ssh_password": [VM password],
      "zabbix_host": [Zabbix host],
      "zabbix_username": [Zabbix username],
      "zabbix_password": [Zabbix password],
      "vyatta_host": [Vyatta host],
      "vyatta_username": [Vyatta username],
      "vyatta_password": [Vyatta password],
    }

4. Run the execution::

    mistral execution-create register_in_multiple_services.create_and_register input.json

5. Using execution id from the previous step wait for completion (workflow
   ``SUCCESS`` state)::

    mistral execution-get <execution_id>

6. Check your Zabbix host group. You will see new host group, one host in it
   and one simple check item. Log in your Vyatta and check Firewall service.
   You will see new accept rule with configured IP address, protocol and port.
