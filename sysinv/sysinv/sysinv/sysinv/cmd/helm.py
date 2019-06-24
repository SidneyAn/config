#!/usr/bin/env python
#
# Copyright (c) 2018 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

"""
System Inventory Helm Utility.
"""

import sys

from oslo_config import cfg
from oslo_log import log

from sysinv.common import service
from sysinv.db import api
from sysinv.helm import helm

CONF = cfg.CONF

LOG = log.getLogger(__name__)


def create_app_overrides_action(path, app_name=None, namespace=None):
    dbapi = api.get_instance()
    operator = helm.HelmOperator(dbapi=dbapi)
    system_apps = operator.get_helm_applications()
    if app_name not in system_apps:
        LOG.info("Overrides generation for application %s is "
                 "not supported via this command." % app_name)
    else:
        operator.generate_helm_application_overrides(path, app_name, mode=None,
                                                     cnamespace=namespace)


def create_armada_app_overrides_action(path, app_name=None, namespace=None):
    dbapi = api.get_instance()
    operator = helm.HelmOperator(dbapi=dbapi)
    system_apps = operator.get_helm_applications()
    if app_name not in system_apps:
        LOG.info("Overrides generation for application %s is "
                 "not supported via this command." % app_name)
    else:
        operator.generate_helm_application_overrides(path, app_name, mode=None,
                                                     cnamespace=namespace,
                                                     armada_format=True,
                                                     armada_chart_info=None,
                                                     combined=False)


def create_chart_override_action(path, chart_name=None, namespace=None):
    dbapi = api.get_instance()
    operator = helm.HelmOperator(dbapi=dbapi)
    operator.generate_helm_chart_overrides(path, chart_name, namespace)


def add_action_parsers(subparsers):
    parser = subparsers.add_parser('create-app-overrides')
    parser.set_defaults(func=create_app_overrides_action)
    parser.add_argument('path', nargs='?')
    parser.add_argument('app_name', nargs='?')
    parser.add_argument('namespace', nargs='?')

    parser = subparsers.add_parser('create-armada-app-overrides')
    parser.set_defaults(func=create_armada_app_overrides_action)
    parser.add_argument('path', nargs='?')
    parser.add_argument('app_name', nargs='?')
    parser.add_argument('namespace', nargs='?')

    parser = subparsers.add_parser('create-chart-overrides')
    parser.set_defaults(func=create_chart_override_action)
    parser.add_argument('path', nargs='?')
    parser.add_argument('chart_name', nargs='?')
    parser.add_argument('namespace', nargs='?')


CONF.register_cli_opt(
    cfg.SubCommandOpt('action',
                      title='actions',
                      help='Perform helm override operation',
                      handler=add_action_parsers))


def main():
    service.prepare_service(sys.argv)
    if CONF.action.name == 'create-app-overrides':
        if not CONF.action.path:
            LOG.error("overrides path is required")
        elif not CONF.action.app_name:
            LOG.error("application name is required")
        else:
            CONF.action.func(CONF.action.path,
                             CONF.action.app_name,
                             CONF.action.namespace)
    elif CONF.action.name == 'create-armada-app-overrides':
        if not CONF.action.path:
            LOG.error("overrides path is required")
        elif not CONF.action.app_name:
            LOG.error("application name is required")
        else:
            CONF.action.func(CONF.action.path,
                             CONF.action.app_name,
                             CONF.action.namespace)
    elif CONF.action.name == 'create-chart-overrides':
        try:
            CONF.action.func(CONF.action.path,
                             CONF.action.chart_name,
                             CONF.action.namespace)
        except Exception as e:
            print(e)
