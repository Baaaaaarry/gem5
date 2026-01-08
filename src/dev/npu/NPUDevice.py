# Copyright (c) 2025
# All rights reserved.
#
# A minimal NPU device model interface for gem5.
#
# This model is intentionally simple: it exposes an MMIO region and a
# DMA-capable interface, but does not implement any real computation.

from m5.objects.Device import DmaVirtDevice
from m5.params import *


class NPUDevice(DmaVirtDevice):
    type = "NPUDevice"
    cxx_header = "dev/npu/npu_device.hh"
    cxx_class = "gem5::NPUDevice"

    # Base address and size of the NPU MMIO window.
    pioAddr = Param.Addr("Base physical address of the NPU MMIO region")
    pioSize = Param.Addr(0x1000, "Size of the NPU MMIO region")

    # Simple fixed MMIO latency.
    pioDelay = Param.Latency("10ns", "Latency for NPU MMIO accesses")
