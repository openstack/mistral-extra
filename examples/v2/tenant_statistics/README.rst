===============================================
Tenant statistics example (based on v2 API/DSL)
===============================================

The example shows how Mistral can be used to gather information about
OpenStack tenant. The workbook ``tenant_statistics`` contains two workflows
that solve the same task: they send an email report containing a number
of virtual machines, number of active virtual machines and number of
networks. Workflow ``tenant_statistics_plain`` runs runs all its tasks
sequentially one after another. Workflow ``tenant_statistics_join`` runs
two tasks in parallel to gather tenant metrics, waits their completion
using ``join`` workflow control and after that sends a report.

To run the example:

1. Load workbook from ``tenant_statistics.yaml``::

        mistral workbook-create tenant_statistics.yaml

2. Create ``input.json`` file containing workflow input parameters as follows::

        {
            "to_email": "admin@my_domain.com",
            "from_email": "my_address@my_domain.com",
            "smtp_server": "smtp.my_domain.com:587",
            "smtp_password": "my_password"
        }

3. Start workflow::

        mistral execution-create tenant_statistics.tenant_statistics_join input.json

4. Using execution id from the previous step wait for completion (workflow ``SUCCESS`` state)::

        mistral execution-get <execution_id>

5. Check email inbox for the expected report.
