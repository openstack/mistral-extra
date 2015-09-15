=================================================
Zabbix registration example (based on v2 API/DSL)
=================================================

The example is created to demonstrate how Mistral can be used to interact
with third party service's API through HTTP requests. This specific example
works with Zabbix monitoring service. Mistral uses auth information provided by
the user to retrieve Zabbix auth token. Then it creates host group (in terms of
Zabbix), host with given machine IP and sets simple check item - ping machine
every 5 seconds.

How to run
----------

1. Load workbook from ``zabbix_machine_registration.yaml``::

    mistral workbook-create zabbix_machine_registration.yaml

2. Create ``input.json`` file containing workflow input::

    {
      "machine_ip": [your machine IP],
      "machine_port": [your machine port],
      "zabbix_host": [Zabbix host],
      "zabbix_username": [Zabbix username],
      "zabbix_password": [Zabbix password],
    }

3. Run the execution::

    mistral execution-create zabbix.register_in_zabbix input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

    mistral execution-get <execution_id>

5. Check your Zabbix host group. You will see new host group, one host in it and one simple check item.
