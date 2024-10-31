#  Copyright 2020 - Nokia Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from mistral_lib.exceptions import MistralException


class UnauthorizedException(MistralException):
    http_code = 401
    message = "Unauthorized"


class ApplicationContextNotFoundException(MistralException):
    http_code = 400
    message = "Application context not found"


class ActionException(MistralException):
    http_code = 400


class MistralKeystoneException(MistralException):
    message = "A unknown Keystone exception occurred"
