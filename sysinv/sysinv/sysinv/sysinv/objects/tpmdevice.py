#
# Copyright (c) 2013-2015 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

# vim: tabstop=4 shiftwidth=4 softtabstop=4
# coding=utf-8
#

from sysinv.db import api as db_api
from sysinv.objects import base
from sysinv.objects import utils


class TPMDevice(base.SysinvObject):

    dbapi = db_api.get_instance()

    fields = {
        'id': int,
        'uuid': utils.str_or_none,
        'state': utils.str_or_none,
        'tpm_data': utils.dict_or_none,

        'host_id': int,
        'host_uuid': utils.str_or_none,
    }

    _foreign_fields = {'host_uuid': 'host:uuid'}

    @base.remotable_classmethod
    def get_by_uuid(cls, context, uuid):
        return cls.dbapi.tpmdevice_get(uuid)

    def save_changes(self, context, updates):
        self.dbapi.tpmdevice_update(self.uuid,  # pylint: disable=no-member
                                    updates)
