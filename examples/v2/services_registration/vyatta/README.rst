=============================================
Vyatta Firewall example (based on v2 API/DSL)
=============================================

The example is created to demonstrate how Mistral can be used to interact
with third party service's API through HTTP requests. This specific example
works with Vyatta Firewall service. Mistral uses auth information provided by
the user to retrieve Vyatta configuration URL. Then it creates accept rule in Firewall
service, sets IP address, protocol and port to this rule and commit transaction.

How to run
----------

1. Load workbook from ``vyatta_firewall.yaml``::

    mistral workbook-create vyatta_firewall.yaml

2. Create ``input.json`` file containing workflow input::

    {
      "machine_ip": [your machine IP],
      "machine_name": [your machine name],
      "port": [Firewall port to open],
      "vyatta_host": [Zabbix host],
      "vyatta_username": [Zabbix username],
      "vyatta_password": [Zabbix password],
    }

3. Run the execution::

    mistral execution-create vyatta.register_in_vyatta_firewall input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

    mistral execution-get <execution_id>

5. Log in your Vyatta and check Firewall service. You will see new accept rule with configured
   IP address, protocol and port.
