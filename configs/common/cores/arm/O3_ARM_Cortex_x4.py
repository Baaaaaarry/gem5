# Copyright (c) 2012, 2017-2018, 2023 Arm Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.objects import *
from m5.objects.ArmMMU import ArmMMU
from m5.proxy import *

from .O3_ARM_v7a import (
    O3_ARM_v7a_3,
    O3_ARM_v7a_DCache,
    O3_ARM_v7a_ICache,
    O3_ARM_v7aL2,
)


class O3_ARM_Cortex_x4(O3_ARM_v7a_3):
    LQEntries = 16
    SQEntries = 16
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = "1024"
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 10
    fetchBufferSize = 16
    fetchToDecodeDelay = 3
    decodeWidth = 10
    decodeToRenameDelay = 1
    renameWidth = 10
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 10
    issueWidth = 10
    wbWidth = 8
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    numPhysIntRegs = 128
    numPhysFloatRegs = 192
    numPhysVecRegs = 48
    numIQEntries = 32
    numROBEntries = 384

    switched_out = False

    mmu = ArmMMU(
        l2_shared=ArmTLB(
            entry_type="unified", size=2048, assoc=4, partial_levels=["L2"]
        ),
        itb=ArmTLB(
            entry_type="instruction", size=48, next_level=Parent.l2_shared
        ),
        dtb=ArmTLB(entry_type="data", size=96, next_level=Parent.l2_shared),
    )


class O3_ARM_Cortex_x4_ICache(O3_ARM_v7a_ICache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 2
    tgts_per_mshr = 8
    size = "64KiB"
    assoc = 4
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


# Data Cache
class O3_ARM_Cortex_x4_DCache(O3_ARM_v7a_DCache):
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 6
    tgts_per_mshr = 8
    size = "64KiB"
    assoc = 4
    write_buffers = 16
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True


# L2 Cache
class O3_ARM_Cortex_x4L2(O3_ARM_v7aL2):
    tag_latency = 12
    data_latency = 12
    response_latency = 12
    mshrs = 16
    tgts_per_mshr = 8
    size = "2MiB"
    assoc = 8
    write_buffers = 8
    clusivity = "mostly_excl"
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency=1, prefetch_on_access=True)
    tags = BaseSetAssoc()
    replacement_policy = RandomRP()
