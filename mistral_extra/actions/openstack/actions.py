# Copyright 2014 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import functools

from oslo_config import cfg
from oslo_log import log
from oslo_utils import importutils

from keystoneauth1.identity import v3 as ks_identity_v3
from keystoneauth1 import session as ks_session
from keystoneauth1.token_endpoint import Token
from keystoneclient import httpclient

from mistral_extra.actions.openstack import base
from mistral_extra.actions.openstack.utils import keystone as keystone_utils
from mistral_lib.utils import inspect_utils

LOG = log.getLogger(__name__)

CONF = cfg.CONF


IRONIC_API_VERSION = '1.34'
"""The default microversion to pass to Ironic API.

1.34 corresponds to Pike final.
"""


def _try_import(module_name):
    try:
        return importutils.try_import(module_name)
    except Exception as e:
        msg = 'Unable to load module "%s". %s' % (module_name, str(e))
        LOG.error(msg)
        return None


aodhclient = _try_import('aodhclient.v2.client')
barbicanclient = _try_import('barbicanclient.client')
cinderclient = _try_import('cinderclient.client')
cinder_api_versions = _try_import('cinderclient.api_versions')
designateclient = _try_import('designateclient.v2.client')
glanceclient = _try_import('glanceclient')
gnocchiclient = _try_import('gnocchiclient.v1.client')
heatclient = _try_import('heatclient.client')
ironic_inspector_client = _try_import('ironic_inspector_client.v1')
ironicclient = _try_import('ironicclient.v1.client')
keystoneclient = _try_import('keystoneclient.v3.client')
manila = _try_import('manilaclient')
manilaclient = _try_import('manilaclient.client')
manila_api_versions = _try_import('manilaclient.api_versions')
magnumclient = _try_import('magnumclient.v1.client')
mistralclient = _try_import('mistralclient.api.v2.client')
muranoclient = _try_import('muranoclient.v1.client')
neutronclient = _try_import('neutronclient.v2_0.client')
nova = _try_import('novaclient')
novaclient = _try_import('novaclient.client')
nova_api_versions = _try_import('novaclient.api_versions')
senlinclient = _try_import('senlinclient.v1.client')
swift_client = _try_import('swiftclient.client')
swiftservice = _try_import('swiftclient.service')
tackerclient = _try_import('tackerclient.v1_0.client')
troveclient = _try_import('troveclient.v1.client')
vitrageclient = _try_import('vitrageclient.v1.client')
zaqarclient = _try_import('zaqarclient.queues.client')
zunclient = _try_import('zunclient.v1.client')
zun_api_versions = _try_import('zunclient.api_versions')


class NovaAction(base.OpenStackAction):
    _service_type = 'compute'

    @classmethod
    def _get_client_class(cls):
        return novaclient.Client

    def _create_client(self, context):
        LOG.debug("Nova action security context: %s", context)

        nova_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        temp_client = self._get_client_class()(
            nova.API_MIN_VERSION,
            endpoint_override=nova_endpoint.url,
            session=session_and_auth['session']
        )

        discovered_version = nova_api_versions.discover_version(
            temp_client,
            nova_api_versions.APIVersion("2.latest")
        )

        return self._get_client_class()(
            discovered_version,
            endpoint_override=nova_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(2)


class GlanceAction(base.OpenStackAction):
    _service_type = 'image'

    @classmethod
    def _get_client_class(cls):
        return glanceclient.Client

    def _create_client(self, context):

        LOG.debug("Glance action security context: %s", context)

        glance_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            '2',
            endpoint=glance_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(endpoint="http://127.0.0.1:9292/v2")


class KeystoneAction(base.OpenStackAction):

    _service_type = 'identity'

    @classmethod
    def _get_client_class(cls):
        return keystoneclient.Client

    def _create_client(self, context):

        LOG.debug("Keystone action security context: %s", context)

        keystone_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            endpoint=keystone_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        # Here we need to replace httpclient authenticate method temporarily
        authenticate = httpclient.HTTPClient.authenticate

        httpclient.HTTPClient.authenticate = lambda x: True
        fake_client = cls._get_client_class()()

        # Once we get fake client, return back authenticate method
        httpclient.HTTPClient.authenticate = authenticate

        return fake_client


class HeatAction(base.OpenStackAction):
    _service_type = 'orchestration'

    @classmethod
    def _get_client_class(cls):
        return heatclient.Client

    def _create_client(self, context):
        LOG.debug("Heat action security context: %s", context)

        heat_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            '1',
            endpoint_override=heat_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            '1',
            endpoint="http://127.0.0.1:8004/v1/fake"
        )


class NeutronAction(base.OpenStackAction):
    _service_type = 'network'

    @classmethod
    def _get_client_class(cls):
        return neutronclient.Client

    def _create_client(self, context):

        LOG.debug("Neutron action security context: %s", context)

        neutron_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            endpoint_override=neutron_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(endpoint="http://127.0.0.1")


class CinderAction(base.OpenStackAction):
    _service_type = 'volumev3'

    @classmethod
    def _get_client_class(cls):
        return cinderclient.Client

    def _create_client(self, context):

        LOG.debug("Cinder action security context: %s", context)

        cinder_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        temp_client = self._get_client_class()(
            cinder_api_versions.MAX_VERSION,
            endpoint_override=cinder_endpoint.url,
            session=session_and_auth['session']
        )

        discovered_version = cinder_api_versions.discover_version(
            temp_client,
            cinder_api_versions.APIVersion(cinder_api_versions.MAX_VERSION),
        )

        return self._get_client_class()(
            discovered_version,
            endpoint_override=cinder_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()('3')


class MistralAction(base.OpenStackAction):
    _service_type = 'workflowv2'

    @classmethod
    def _get_client_class(cls):
        return mistralclient.Client

    def _create_client(self, context):

        LOG.debug("Mistral action security context: %s", context)

        if CONF.pecan.auth_enable:
            session_and_auth = self.get_session_and_auth(context)

            return self._get_client_class()(
                mistral_url=session_and_auth['auth'].endpoint,
                **session_and_auth)
        else:
            mistral_url = 'http://{}:{}/v2'.format(CONF.api.host,
                                                   CONF.api.port)
            return self._get_client_class()(mistral_url=mistral_url)

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class TroveAction(base.OpenStackAction):
    _service_type = 'database'

    @classmethod
    def _get_client_class(cls):
        return troveclient.Client

    def _create_client(self, context):

        LOG.debug("Trove action security context: %s", context)

        trove_endpoint = self.get_service_endpoint()

        trove_url = keystone_utils.format_url(
            trove_endpoint.url,
            {'tenant_id': context.project_id}
        )

        client = self._get_client_class()(
            context.user_name,
            context.auth_token,
            project_id=context.project_id,
            auth_url=trove_url,
            region_name=trove_endpoint.region,
            insecure=context.insecure
        )

        client.client.auth_token = context.auth_token
        client.client.management_url = trove_url

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("fake_user", "fake_passwd")


class IronicAction(base.OpenStackAction):
    _service_name = 'ironic'

    @classmethod
    def _get_client_class(cls):
        return ironicclient.Client

    def _create_client(self, context):

        LOG.debug("Ironic action security context: %s", context)

        ironic_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        client = self._get_client_class()(
            os_ironic_api_version=IRONIC_API_VERSION,
            endpoint_override=ironic_endpoint.url,
            session=session_and_auth['session']
        )

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            endpoint_override="http://127.0.0.1:6385/",
            session=ks_session.Session(),
        )


class BaremetalIntrospectionAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return ironic_inspector_client.ClientV1

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(inspector_url='http://127.0.0.1')

    def _create_client(self, context):
        LOG.debug(
            "Baremetal introspection action security context: %s", context)

        inspector_endpoint = keystone_utils.get_endpoint_for_project(
            service_type='baremetal-introspection'
        )
        auth = Token(endpoint=inspector_endpoint.url,
                     token=context.auth_token)

        return self._get_client_class()(
            api_version=1,
            session=ks_session.Session(auth)
        )


class SwiftAction(base.OpenStackAction):
    _service_name = 'swift'

    @classmethod
    def _get_client_class(cls):
        return swift_client.Connection

    def _create_client(self, context):

        LOG.debug("Swift action security context: %s", context)

        swift_endpoint = self.get_service_endpoint()

        swift_url = keystone_utils.format_url(
            swift_endpoint.url,
            {'tenant_id': context.project_id}
        )

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            session=session_and_auth['session'],
            preauthurl=swift_url
        )


class SwiftServiceAction(base.OpenStackAction):
    _service_name = 'swift'

    @classmethod
    def _get_client_class(cls):
        return swiftservice.SwiftService

    def _create_client(self, context):

        LOG.debug("Swift action security context: %s", context)

        swift_endpoint = self.get_service_endpoint()

        swift_opts = {
            'os_storage_url': swift_endpoint.url % {
                'tenant_id': context.project_id
            },
            'os_auth_token': context.auth_token,
            'os_region_name': swift_endpoint.region,
            'os_project_id': context.security.project_id,
        }

        return swiftservice.SwiftService(options=swift_opts)

    @classmethod
    def _get_client_method(cls, client):
        return getattr(client, cls.client_method_name)


class ZaqarAction(base.OpenStackAction):
    _service_type = 'messaging'

    @classmethod
    def _get_client_class(cls):
        return zaqarclient.Client

    def _create_client(self, context):
        LOG.debug("Zaqar action security context: %s", context)

        zaqar_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            version=2,
            url=zaqar_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(version=2)

    @classmethod
    def _get_client_method(cls, client):
        method = getattr(cls, cls.client_method_name)

        # We can't use partial as it's not supported by getargspec
        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return method(client, *args, **kwargs)

        arguments = inspect_utils.get_arg_list_as_str(method)
        # Remove client
        wrap.__arguments__ = arguments.split(', ', 1)[1]

        return wrap

    @staticmethod
    def queue_messages(client, queue_name, **params):
        """Gets a list of messages from the queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param params: Filters to use for getting messages.
        :type params: **kwargs dict

        :returns: List of messages.
        :rtype: `list`
        """
        queue = client.queue(queue_name)

        return queue.messages(**params)

    @staticmethod
    def queue_post(client, queue_name, messages):
        """Posts one or more messages to a queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param messages: One or more messages to post.
        :type messages: `list` or `dict`

        :returns: A dict with the result of this operation.
        :rtype: `dict`
        """
        queue = client.queue(queue_name)

        return queue.post(messages)

    @staticmethod
    def queue_pop(client, queue_name, count=1):
        """Pop `count` messages from the queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param count: Number of messages to pop.
        :type count: int

        :returns: List of messages.
        :rtype: `list`
        """
        queue = client.queue(queue_name)

        return queue.pop(count)

    @staticmethod
    def claim_messages(client, queue_name, **params):
        """Claim messages from the queue

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :returns: List of claims
        :rtype: `list`
        """
        queue = client.queue(queue_name)
        return queue.claim(**params)

    @staticmethod
    def delete_messages(client, queue_name, messages):
        """Delete messages from the queue

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param messages: List of messages' ids to delete.
        :type messages: *args of `six.string_type`

        :returns: List of messages' ids that have been deleted
        :rtype: `list`
        """
        queue = client.queue(queue_name)
        return queue.delete_messages(*messages)


class BarbicanAction(base.OpenStackAction):
    _service_type = 'key-manager'

    @classmethod
    def _get_client_class(cls):
        return barbicanclient.Client

    def _create_client(self, context):
        LOG.debug("Barbican action security context: %s", context)

        barbican_endpoint = self.get_service_endpoint()
        session_and_auth = self.get_session_and_auth(context)

        return self._get_client_class()(
            endpoint=barbican_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            project_id="1",
            endpoint="http://127.0.0.1:9311"
        )

    @classmethod
    def _get_client_method(cls, client):
        if cls.client_method_name not in ["secrets_store",
                                          "secrets_retrieve"]:
            return super(BarbicanAction, cls)._get_client_method(client)

        method = getattr(cls, cls.client_method_name)

        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return method(client, *args, **kwargs)

        arguments = inspect_utils.get_arg_list_as_str(method)

        # Remove client.
        wrap.__arguments__ = arguments.split(', ', 1)[1]

        return wrap

    @staticmethod
    def secrets_store(client,
                      name=None,
                      payload=None,
                      algorithm=None,
                      bit_length=None,
                      secret_type=None,
                      mode=None, expiration=None):
        """Create and Store a secret in Barbican.

        :param client: the Barbican client
        :type client: barbicanclient.client

        :param name: A friendly name for the Secret
        :type name: string

        :param payload: The unencrypted secret data
        :type payload: string

        :param algorithm: The algorithm associated with this secret key
        :type algorithm: string

        :param bit_length: The bit length of this secret key
        :type bit_length: int

        :param secret_type: The secret type for this secret key
        :type secret_type: string

         :param mode: The algorithm mode used with this secret keybit_length:
        :type mode: string

        :param expiration: The expiration time of the secret in ISO 8601 format
        :type expiration: string

        :returns: A new Secret object
        :rtype: class:`barbicanclient.secrets.Secret'
        """

        entity = client.secrets.create(
            name,
            payload,
            algorithm,
            bit_length,
            secret_type,
            mode,
            expiration
        )

        entity.store()

        return entity._get_formatted_entity()

    @staticmethod
    def secrets_retrieve(client, secret_ref):
        """Retrieve the payload from a secret in Barbican.

        :param client: the Barbican client
        :type client: barbicanclient.client

        :param secret_ref: Full HATEOAS reference to a Secret
        :type secret_ref: string
        """

        return client.secrets.get(secret_ref).payload


class DesignateAction(base.OpenStackAction):
    _service_type = 'dns'

    @classmethod
    def _get_client_class(cls):
        return designateclient.Client

    def _create_client(self, context):
        LOG.debug("Designate action security context: %s", context)

        session_and_auth = self.get_session_and_auth(context)

        client = self._get_client_class()(
            session=session_and_auth['session']
        )

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            endpoint_override="http://127.0.0.1:9001/",
            session=ks_session.Session()
        )


class MagnumAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return magnumclient.Client

    def _create_client(self, context):

        LOG.debug("Magnum action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint()
        auth_url = keystone_endpoint.url
        magnum_url = keystone_utils.get_endpoint_for_project('magnum').url

        return self._get_client_class()(
            magnum_url=magnum_url,
            auth_token=context.auth_token,
            project_id=context.project_id,
            auth_url=auth_url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(auth_url='X', magnum_url='X')


class MuranoAction(base.OpenStackAction):
    _service_name = 'murano'

    @classmethod
    def _get_client_class(cls):
        return muranoclient.Client

    def _create_client(self, context):

        LOG.debug("Murano action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint()
        murano_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint=murano_endpoint.url,
            token=context.auth_token,
            tenant=context.project_id,
            region_name=murano_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("http://127.0.0.1:8082/")


class TackerAction(base.OpenStackAction):
    _service_name = 'tacker'

    @classmethod
    def _get_client_class(cls):
        return tackerclient.Client

    def _create_client(self, context):

        LOG.debug("Tacker action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint()
        tacker_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint_url=tacker_endpoint.url,
            token=context.auth_token,
            tenant_id=context.project_id,
            region_name=tacker_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class SenlinAction(base.OpenStackAction):
    _service_name = 'senlin'

    @classmethod
    def _get_client_class(cls):
        return senlinclient.Client

    def _create_client(self, context):

        LOG.debug("Senlin action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint()
        senlin_endpoint = self.get_service_endpoint()

        if context.is_trust_scoped and keystone_utils.is_token_trust_scoped(
                context.auth_token):
            if context.trust_id is None:
                raise Exception(
                    "'trust_id' must be provided in the admin context."
                )

            auth = ks_identity_v3.Password(
                auth_url=keystone_endpoint.url,
                trust_id=context.trust_id,
                username=CONF.keystone_authtoken.username,
                password=CONF.keystone_authtoken.password,
                user_domain_name=CONF.keystone_authtoken.user_domain_name
            )
        else:
            auth = ks_identity_v3.Token(
                auth_url=keystone_endpoint.url,
                token=context.auth_token,
                project_id=context.project_id
            )

        return self._get_client_class()(
            endpoint_url=senlin_endpoint.url,
            session=ks_session.Session(auth=auth),
            tenant_id=context.project_id,
            region_name=senlin_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        # Senlin client changed interface a bit, let's skip __init__ altogether
        class_ = cls._get_client_class()
        return class_.__new__(class_)


class AodhAction(base.OpenStackAction):
    _service_type = 'alarming'

    @classmethod
    def _get_client_class(cls):
        return aodhclient.Client

    def _create_client(self, context):

        LOG.debug("Aodh action security context: %s", context)

        aodh_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            aodh_endpoint.url,
            {'tenant_id': context.project_id}
        )

        return self._get_client_class()(
            endpoint_url,
            region_name=aodh_endpoint.region,
            token=context.auth_token,
            username=context.user_name,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class GnocchiAction(base.OpenStackAction):
    _service_type = 'metric'

    @classmethod
    def _get_client_class(cls):
        return gnocchiclient.Client

    def _create_client(self, context):
        LOG.debug("Gnocchi action security context: %s", context)

        gnocchi_endpoint = keystone_utils.get_endpoint_for_project(
            service_type="metric")
        keystone_endpoint = keystone_utils.get_keystone_endpoint()

        auth = ks_identity_v3.Token(
            auth_url=keystone_endpoint.url,
            tenant_name=context.user_name,
            token=context.auth_token,
            tenant_id=context.project_id
        )

        return self._get_client_class()(
            adapter_options={"region_name": gnocchi_endpoint.region,
                             "project_id": context.project_id,
                             "endpoint": gnocchi_endpoint.url,
                             "insecure": context.insecure},
            session_options={"auth": auth}
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class VitrageAction(base.OpenStackAction):
    _service_type = 'rca'

    @classmethod
    def _get_client_class(cls):
        return vitrageclient.Client

    def _create_client(self, context):

        LOG.debug("Vitrage action security context: %s", context)

        vitrage_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            vitrage_endpoint.url,
            {'tenant_id': context.project_id}
        )

        session_and_auth = self.get_session_and_auth(context)

        return vitrageclient.Client(
            session=session_and_auth['session'],
            endpoint_override=endpoint_url
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class ZunAction(base.OpenStackAction):
    _service_name = 'appcontainer'

    @classmethod
    def _get_client_class(cls):
        return zunclient.Client

    def _create_client(self, context):

        LOG.debug("Zun action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint()
        zun_endpoint = self.get_service_endpoint()
        session_and_auth = self.get_session_and_auth(context)

        temp_client = self._get_client_class()(
            zun_api_versions.MAX_API_VERSION,
            endpoint_override=zun_endpoint.url,
            auth_url=keystone_endpoint.url,
            session=session_and_auth['auth']
        )

        discovered_version = zun_api_versions.discover_version(
            temp_client,
            zun_api_versions.APIVersion(zun_api_versions.MAX_API_VERSION)
        )

        return self._get_client_class()(
            discovered_version,
            endpoint_override=zun_endpoint.url,
            auth_url=keystone_endpoint.url,
            session=session_and_auth['session']
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            endpoint_override="http://127.0.0.1:9517/",
            session=ks_session.Session()
        )


class ManilaAction(base.OpenStackAction):
    _service_type = 'sharev2'

    @classmethod
    def _get_client_class(cls):
        return manilaclient.Client

    def _create_client(self, context):

        LOG.debug("Manila action security context: %s", context)

        manila_endpoint = self.get_service_endpoint()

        session_and_auth = self.get_session_and_auth(context)

        temp_client = self._get_client_class()(
            manila.API_MAX_VERSION,
            service_catalog_url=manila_endpoint.url,
            session=session_and_auth['auth']
        )

        discovered_version = manila_api_versions.discover_version(
            temp_client,
            manila.API_MAX_VERSION
        )

        client = self._get_client_class()(
            discovered_version,
            service_catalog_url=manila_endpoint.url,
            session=session_and_auth['session']
        )

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            manila.API_MAX_VERSION,
            input_auth_token='token',
            service_catalog_url='http://127.0.0.1:8786')
