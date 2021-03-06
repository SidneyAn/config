#
# Copyright (c) 2020 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import constants

# PCI Device Class ID in hexidecimal string
PCI_DEVICE_CLASS_FPGA = '120000'

# Device Vendors
PCI_DEVICE_VENDOR_INTEL = "8086"

# Device Ids
PCI_DEVICE_ID_FPGA_INTEL_5GNR_FEC_PF = "0d8f"
PCI_DEVICE_ID_FPGA_INTEL_5GNR_FEC_VF = "0d90"

# SR-IOV enabled devices
SRIOV_ENABLED_DEVICE_IDS = [PCI_DEVICE_ID_FPGA_INTEL_5GNR_FEC_PF]

FPGA_INTEL_5GNR_FEC_DRIVER_IGB_UIO = "igb_uio"
FPGA_INTEL_5GNR_FEC_DRIVER_NONE = "none"

FPGA_INTEL_5GNR_FEC_VF_VALID_DRIVERS = [FPGA_INTEL_5GNR_FEC_DRIVER_IGB_UIO,
                                        constants.SRIOV_DRIVER_TYPE_VFIO,
                                        FPGA_INTEL_5GNR_FEC_DRIVER_NONE]
FPGA_INTEL_5GNR_FEC_PF_VALID_DRIVERS = [FPGA_INTEL_5GNR_FEC_DRIVER_IGB_UIO,
                                        FPGA_INTEL_5GNR_FEC_DRIVER_NONE]

# Device Image
DEVICE_IMAGE_TMP_PATH = '/tmp/device_images'
DEVICE_IMAGE_PATH = '/opt/platform/device_images'

BITSTREAM_TYPE_ROOT_KEY = 'root-key'
BITSTREAM_TYPE_FUNCTIONAL = 'functional'
BITSTREAM_TYPE_KEY_REVOCATION = 'key-revocation'

# Device Image Status
DEVICE_IMAGE_UPDATE_PENDING = 'pending'
DEVICE_IMAGE_UPDATE_IN_PROGRESS = 'in-progress'
DEVICE_IMAGE_UPDATE_IN_PROGRESS_ABORTED = 'in-progress-aborted'
DEVICE_IMAGE_UPDATE_COMPLETED = 'completed'
DEVICE_IMAGE_UPDATE_FAILED = 'failed'
DEVICE_IMAGE_UPDATE_NULL = ''

# Device Image Action
APPLY_ACTION = 'apply'
REMOVE_ACTION = 'remove'
