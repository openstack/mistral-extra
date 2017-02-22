# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import flask


app = flask.Flask(__name__)
host = "0.0.0.0"
port = 5000


@app.route('/summ', methods=["POST"])
def summ():
    summ = 0
    args = flask.request.data

    try:
        args_list = flask.json.loads(args).get('arguments')
    except Exception:
        return (403, "Please, specify list of arguments in the request body"
                " in form '{\"arguments\": [arg1, arg2, .., argN]}'")

    for a in args_list:
        try:
            summ += int(a)
        except Exception:
            return 403, "Sorry, need to use only integer arguments!"

    return flask.jsonify({'result': summ})


if __name__ == "__main__":
    app.run(host=host, port=port)
