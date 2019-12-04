# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2010 OpenStack Foundation
# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
from oslo_utils import importutils


glance_opts = [
    cfg.StrOpt('glance_host',
               default='$my_ip',
               help='default glance hostname or ip'),
    cfg.IntOpt('glance_port',
               default=9292,
               help='default glance port'),
    cfg.StrOpt('glance_protocol',
               default='http',
               help='Default protocol to use when connecting to glance. '
               'Set to https for SSL.'),
    cfg.StrOpt('glance_api_servers',
               help='A list of the glance api servers available to nova. '
               'Prefix with https:// for ssl-based glance api servers. '
               '([hostname|ip]:port)'),
    cfg.BoolOpt('glance_api_insecure',
                default=False,
                help='Allow to perform insecure SSL (https) requests to '
                     'glance'),
    cfg.IntOpt('glance_num_retries',
               default=0,
               help='Number retries when downloading an image from glance'),
    cfg.StrOpt('auth_strategy',
               default='keystone',
               help='Default protocol to use when connecting to glance. '
               'Set to https for SSL.'),
]


CONF = cfg.CONF
CONF.register_opts(glance_opts, group='glance')


def import_versioned_module(version, submodule=None):
    module = 'sysinv.common.glance_service.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def Service(client=None, version=1, context=None):
    module = import_versioned_module(version, 'image_service')
    service_class = getattr(module, 'GlanceImageService')
    return service_class(client, version, context)
