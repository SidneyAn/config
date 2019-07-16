#
# Copyright (c) 2019 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import constants
from sysinv.common import exception
from sysinv.openstack.common import log as logging
from sysinv.helm import common
from sysinv.helm import openstack

LOG = logging.getLogger(__name__)


class KeystoneApiProxyHelm(openstack.OpenstackBaseHelm):
    """Class to encapsulate helm operations for the keystone api proxy chart"""

    CHART = constants.HELM_CHART_KEYSTONE_API_PROXY

    SERVICE_NAME = constants.HELM_CHART_KEYSTONE_API_PROXY
    DCORCH_SERVICE_NAME = 'dcorch'

    def execute_manifest_updates(self, operator, app_name=None):
        if (self._distributed_cloud_role() ==
                constants.DISTRIBUTED_CLOUD_ROLE_SYSTEMCONTROLLER):
            operator.manifest_chart_groups_insert(
                'armada-manifest', 'openstack-keystone-api-proxy')

    def get_overrides(self, namespace=None):
        overrides = {
            common.HELM_NS_OPENSTACK: {
                'pod': {
                    'user': {
                        'keystone_api_proxy': {
                            'uid': 0
                        }
                    }
                },
                'conf': {
                    'keystone_api_proxy': {
                        'DEFAULT': {
                            'transport_url': self._get_transport_url()
                        },
                        'database': {
                            'connection': self._get_database_connection()
                        },
                        'identity': {
                            'remote_host': self._get_keystone_endpoint(),
                        }
                    }
                },
                'endpoints': self._get_endpoints_overrides(),
            }
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides

    def _get_endpoints_overrides(self):
        return {
            'identity': {
                'auth': self._get_endpoints_identity_overrides(
                    self.SERVICE_NAME, [])
            },
            'keystone_api_proxy': {
                'host_fqdn_override':
                    self._get_endpoints_host_fqdn_overrides(
                        constants.HELM_CHART_KEYSTONE_API_PROXY),
                'port': self._get_endpoints_port_api_public_overrides(),
                'scheme': self._get_endpoints_scheme_public_overrides(),
            }
        }

    def _get_transport_url(self):
        host_url = self._format_url_address(self._get_management_address())
        auth_password = self._get_keyring_password('amqp', 'rabbit')
        transport_url = "rabbit://guest:%s@%s:5672" % (auth_password, host_url)
        return transport_url

    def _get_database_connection(self):
        host_url = self._format_url_address(self._get_management_address())
        auth_password = self._get_keyring_password(
            self.DCORCH_SERVICE_NAME, 'database')
        connection = "postgresql+psycopg2://admin-dcorch:%s@%s/dcorch" %\
                     (auth_password, host_url)
        return connection

    def _get_keystone_endpoint(self):
        return 'keystone-api.openstack.svc.cluster.local'
