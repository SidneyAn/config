#
# Copyright (c) 2017-2018 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

""" System Inventory Puppet Configuration Operator."""

from __future__ import absolute_import

import eventlet
import os
import tempfile
import yaml

from stevedore import extension

from sysinv.openstack.common import log as logging
from sysinv.puppet import common


LOG = logging.getLogger(__name__)


def puppet_context(func):
    """Decorate to initialize the local threading context"""
    def _wrapper(self, *args, **kwargs):
        thread_context = eventlet.greenthread.getcurrent()
        setattr(thread_context, '_puppet_context', dict())
        func(self, *args, **kwargs)
    return _wrapper


class PuppetOperator(object):
    """Class to encapsulate puppet operations for System Inventory"""

    def __init__(self, dbapi=None, path=None):
        if path is None:
            path = common.PUPPET_HIERADATA_PATH

        self.dbapi = dbapi
        self.path = path

        puppet_plugins = extension.ExtensionManager(
            namespace='systemconfig.puppet_plugins',
            invoke_on_load=True, invoke_args=(self,))
        self.puppet_plugins = sorted(puppet_plugins, key=lambda x: x.name)

        for plugin in self.puppet_plugins:
            plugin_name = plugin.name[4:]
            setattr(self, plugin_name, plugin.obj)
            LOG.debug("Loaded puppet plugin %s" % plugin.name)

    @property
    def context(self):
        thread_context = eventlet.greenthread.getcurrent()
        return getattr(thread_context, '_puppet_context')

    @property
    def config(self):
        return self.context.get('config', {})

    @puppet_context
    def create_static_config(self):
        """
        Create the initial static configuration that sets up one-time
        configuration items that are not generated by standard system
        configuration. This is invoked once during initial bootstrap to
        create the required parameters.
        """

        # use the temporary keyring storage during bootstrap phase
        os.environ["XDG_DATA_HOME"] = "/tmp"

        try:
            self.context['config'] = config = {}
            for puppet_plugin in self.puppet_plugins:
                config.update(puppet_plugin.obj.get_static_config())

            filename = 'static.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create static config")
            raise

    @puppet_context
    def create_secure_config(self):
        """
        Create the secure config, for storing passwords.
        This is invoked once during initial bootstrap to
        create the required parameters.
        """

        # use the temporary keyring storage during bootstrap phase
        os.environ["XDG_DATA_HOME"] = "/tmp"

        try:
            self.context['config'] = config = {}
            for puppet_plugin in self.puppet_plugins:
                config.update(puppet_plugin.obj.get_secure_static_config())

            filename = 'secure_static.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create secure config")
            raise

    @puppet_context
    def update_system_config(self):
        """Update the configuration for the system"""
        try:
            # NOTE: order is important due to cached context data
            self.context['config'] = config = {}
            for puppet_plugin in self.puppet_plugins:
                config.update(puppet_plugin.obj.get_system_config())

            filename = 'system.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create system config")
            raise

    @puppet_context
    def update_secure_system_config(self):
        """Update the secure configuration for the system"""
        try:
            # NOTE: order is important due to cached context data
            self.context['config'] = config = {}
            for puppet_plugin in self.puppet_plugins:
                config.update(puppet_plugin.obj.get_secure_system_config())

            filename = 'secure_system.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create secure_system config")
            raise

    @puppet_context
    def update_host_config(self, host, config_uuid=None):
        """Update the host hiera configuration files for the supplied host"""

        self.config_uuid = config_uuid
        self.context['config'] = config = {}
        LOG.info("Updating hiera for host: %s "
                 "with config_uuid: %s" % (host.hostname, config_uuid))
        for puppet_plugin in self.puppet_plugins:
            config.update(puppet_plugin.obj.get_host_config(host))

        self._write_host_config(host, config)

    def remove_host_config(self, host):
        """Remove the configuration for the supplied host"""
        try:
            filename = "%s.yaml" % host.mgmt_ip
            self._remove_config(filename)
        except Exception:
            LOG.exception("failed to remove host config: %s" % host.uuid)

    def _write_host_config(self, host, config):
        """Update the configuration for a specific host"""
        filename = "%s.yaml" % host.mgmt_ip
        self._write_config(filename, config)

    def _write_config(self, filename, config):
        filepath = os.path.join(self.path, filename)
        try:
            fd, tmppath = tempfile.mkstemp(dir=self.path, prefix=filename,
                                           text=True)
            with open(tmppath, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            os.close(fd)
            os.rename(tmppath, filepath)
        except Exception:
            LOG.exception("failed to write config file: %s" % filepath)
            raise

    def _remove_config(self, filename):
        filepath = os.path.join(self.path, filename)
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
        except Exception:
            LOG.exception("failed to delete config file: %s" % filepath)
            raise
