from m5.objects import *
from m5.objects.ArmMMU import ArmMMU
from m5.proxy import *


# Simple ALU Instructions have a latency of 1
class O3_ARM_Cortex_x3_Simple_Int(FUDesc):
    opList = [OpDesc(opClass="IntAlu", opLat=1)]
    count = 4


# Complex ALU instructions have a variable latencies
class O3_ARM_Cortex_x3_Complex_Int(FUDesc):
    opList = [
        OpDesc(opClass="IntMult", opLat=3, pipelined=True),
        OpDesc(opClass="IntDiv", opLat=12, pipelined=False),
        OpDesc(opClass="IprAccess", opLat=3, pipelined=True),
    ]
    count = 2


# Floating point and SIMD instructions
class O3_ARM_Cortex_x3_FP(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=5),
        OpDesc(opClass="FloatCmp", opLat=5),
        OpDesc(opClass="FloatCvt", opLat=5),
        OpDesc(opClass="FloatDiv", opLat=9, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=33, pipelined=False),
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),

    ]
    count = 4

class O3_ARM_Cortex_x3_SIMD(SIMD_Unit):
    count = 2
    
# Load/Store Units
class O3_ARM_Cortex_x3_Load(FUDesc):
    opList = [
        OpDesc(opClass="MemRead", opLat=2),
        OpDesc(opClass="FloatMemRead", opLat=2),
    ]
    count = 2


class O3_ARM_Cortex_x3_Store(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite", opLat=2),
        OpDesc(opClass="FloatMemWrite", opLat=2),
    ]
    count = 3


# Functional Units for this CPU
class O3_ARM_Cortex_x3_FUP(FUPool):
    FUList = [
        O3_ARM_Cortex_x3_Simple_Int(),
        O3_ARM_Cortex_x3_Complex_Int(),
        O3_ARM_Cortex_x3_Load(),
        O3_ARM_Cortex_x3_Store(),
        O3_ARM_Cortex_x3_FP(),
        O3_ARM_Cortex_x3_SIMD(),
    ]


class O3_ARM_Cortex_x3_BTB(SimpleBTB):
    numEntries = 4096
    tagBits = 18
    associativity = 2
    instShiftAmt = 2
    btbReplPolicy = LRURP()
    btbIndexingPolicy = BTBSetAssociative(
        num_entries=Parent.numEntries,
        set_shift=Parent.instShiftAmt,
        assoc=Parent.associativity,
        tag_bits=Parent.tagBits,
    )


# Bi-Mode Branch Predictor with enhanced parameters
class O3_ARM_Cortex_x3_BP(BiModeBP):
    btb = O3_ARM_Cortex_x3_BTB()
    ras = ReturnAddrStack(numEntries=32)
    globalPredictorSize = 16384
    globalCtrBits = 2
    choicePredictorSize = 16384
    choiceCtrBits = 2
    instShiftAmt = 2


class O3_ARM_Cortex_x3(ArmO3CPU):
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
    fetchWidth = 6
    fetchBufferSize = 16
    fetchToDecodeDelay = 3
    decodeWidth = 6
    decodeToRenameDelay = 1
    renameWidth = 8
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 8
    issueWidth = 8
    wbWidth = 8
    fuPool = O3_ARM_Cortex_x3_FUP()
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
    numROBEntries = 320

    switched_out = False
    branchPred = O3_ARM_Cortex_x3_BP()

    mmu = ArmMMU(
        l2_shared=ArmTLB(
            entry_type="unified", size=2048, assoc=4, partial_levels=["L2"]
        ),
        itb=ArmTLB(
            entry_type="instruction", size=48, next_level=Parent.l2_shared
        ),
        dtb=ArmTLB(entry_type="data", size=48, next_level=Parent.l2_shared),
    )


# Instruction Cache
class O3_ARM_Cortex_x3_ICache(Cache):
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
class O3_ARM_Cortex_x3_DCache(Cache):
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
class O3_ARM_Cortex_x3L2(Cache):
    tag_latency = 6
    data_latency = 6
    response_latency = 6
    mshrs = 16
    tgts_per_mshr = 8
    size = "1MiB"
    assoc = 8
    write_buffers = 8
    clusivity = "mostly_excl"
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency=1, prefetch_on_access=True)
    tags = BaseSetAssoc()
    replacement_policy = RandomRP()

class O3_ARM_Cortex_x3_L3(Cache):
    size = "32MiB"
    assoc = 16
    tag_latency = 7
    data_latency = 7
    response_latency = 7
    mshrs = 20
    tgts_per_mshr = 12
    write_buffers = 16
    clusivity = "mostly_excl"