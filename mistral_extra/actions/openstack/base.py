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

import abc
import inspect
import traceback

from oslo_log import log

from mistral_extra.actions.openstack.utils import exceptions as exc
from mistral_extra.actions.openstack.utils import keystone as \
    keystone_utils
from mistral_lib import actions
from mistral_lib.actions import base as ml_actions_base
from mistral_lib import serialization


LOG = log.getLogger(__name__)


class OpenStackAction(actions.Action):
    """OpenStack Action.

    OpenStack Action is the basis of all OpenStack-specific actions,
    which are constructed via OpenStack Action generators.
    """
    _kwargs_for_run = {}
    client_method_name = None
    _service_name = None
    _service_types = []
    _client_class = None

    def __init__(self, **kwargs):
        super(OpenStackAction, self).__init__()

        self._kwargs_for_run = kwargs
        self.action_region = self._kwargs_for_run.pop('action_region', None)

    @abc.abstractmethod
    def _create_client(self, context):
        """Creates client required for action operation."""
        return None

    @classmethod
    def _get_client_class(cls):
        return cls._client_class

    @classmethod
    def _get_client_method(cls, client):
        hierarchy_list = cls.client_method_name.split('.')
        attribute = client

        for attr in hierarchy_list:
            attribute = getattr(attribute, attr)

        return attribute

    @classmethod
    def _get_fake_client(cls):
        """Returns python-client instance which initiated via wrong args.

        It is needed for getting client-method args and description for
        saving into DB.
        """
        # Default is simple _get_client_class instance
        return cls._get_client_class()()

    @classmethod
    def get_fake_client_method(cls):
        return cls._get_client_method(cls._get_fake_client())

    def _get_client(self, context):
        """Returns python-client instance via cache or creation

        Gets client instance according to specific OpenStack Service
        (e.g. Nova, Glance, Heat, Keystone etc)

        """
        return self._create_client(context)

    def get_session_and_auth(self, context):
        """Get keystone session and auth parameters.

        :param context: the action context
        :return: dict that can be used to initialize service clients
        """
        sess = None
        # We try to find the session based on service_types first
        if self._service_types:
            for service_type in self._service_types:
                try:
                    sess = keystone_utils.get_session_and_auth(
                        service_name=None,
                        service_type=service_type,
                        region_name=self.action_region,
                        ctx=context)
                except exc.MistralKeystoneException:
                    # Maybe this service_type was not found
                    pass
        else:
            # Let's use service_name as fallback
            try:
                sess = keystone_utils.get_session_and_auth(
                    service_name=self._service_name,
                    service_type=None,
                    region_name=self.action_region,
                    ctx=context)
            except exc.MistralKeystoneException:
                # Maybe this service_name was not found
                pass

        if not sess:
            raise exc.MistralException(
                "Unable to get keystone session. Maybe endpoints are "
                "missing? (service_name=%s, service_types=%s,"
                " region_name=%s)"
                % (self._service_name, self._service_types,
                   self.action_region)
            )

        return sess

    def get_service_endpoint(self):
        """Get OpenStack service endpoint.

        'service_name' and 'service_type' are defined in specific OpenStack
        service action.
        """
        endpoint = None
        # We try to find the endpoint based on service_types first
        if self._service_types:
            for service_type in self._service_types:
                try:
                    endpoint = keystone_utils.get_endpoint_for_project(
                        service_name=None,
                        service_type=service_type,
                        region_name=self.action_region
                    )
                except exc.MistralKeystoneException:
                    # Maybe this service_type was not found
                    pass
        else:
            # Let's use service_name as fallback
            try:
                endpoint = keystone_utils.get_endpoint_for_project(
                    service_name=self._service_name,
                    service_type=None,
                    region_name=self.action_region
                )
            except exc.MistralKeystoneException:
                # Maybe this service_name was not found
                pass

        if not endpoint:
            raise exc.MistralException(
                "Unable to get service endpoint. Maybe endpoints are "
                "missing? (service_name=%s, service_types=%s,"
                " region_name=%s)"
                % (self._service_name, self._service_types,
                   self.action_region)
            )

        return endpoint

    def run(self, context):
        try:
            method = self._get_client_method(self._get_client(context))

            result = method(**self._kwargs_for_run)

            if inspect.isgenerator(result):
                return [v for v in result]

            return result
        except Exception as e:
            # Print the traceback for the last exception so that we can see
            # where the issue comes from.
            LOG.warning(traceback.format_exc())

            raise exc.ActionException(
                "%s.%s failed: %s" %
                (self.__class__.__name__, self.client_method_name, str(e))
            )

    def test(self, context):
        return dict(
            zip(self._kwargs_for_run, ['test'] * len(self._kwargs_for_run))
        )

    @classmethod
    def get_serialization_key(cls):
        return "%s.%s" % (OpenStackAction.__module__, OpenStackAction.__name__)


class OpenStackActionSerializer(ml_actions_base.ActionSerializer):
    def serialize_to_dict(self, entity):
        res = super(OpenStackActionSerializer, self).serialize_to_dict(entity)

        # Since all OpenStack actions are dynamically generated with the
        # function type() we need to take the base class of the action
        # class (i.e. NovaAction) and write it to the result dict.
        base_cls = type(entity).__bases__[0]

        res['cls'] = '%s.%s' % (base_cls.__module__, base_cls.__name__)

        return res


serialization.register_serializer(OpenStackAction, OpenStackActionSerializer())
