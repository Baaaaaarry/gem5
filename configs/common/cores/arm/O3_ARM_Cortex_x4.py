from m5.objects import *
from m5.objects.ArmMMU import ArmMMU
from m5.proxy import *

# Simple ALU Instructions have a latency of 1
class O3_ARM_Cortex_x4_Simple_Int(FUDesc):
    opList = [OpDesc(opClass="IntAlu", opLat=1)]
    count = 6

# Complex ALU instructions have a variable latencies
class O3_ARM_Cortex_x4_Complex_Int(FUDesc):
    opList = [
        OpDesc(opClass="IntMult", opLat=3, pipelined=True),
        OpDesc(opClass="IntDiv", opLat=12, pipelined=False),
        OpDesc(opClass="IprAccess", opLat=3, pipelined=True),
    ]
    count = 2

# Floating point and SIMD instructions
class O3_ARM_Cortex_x4_FP(FUDesc):
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
class O3_ARM_Cortex_x4_Load(FUDesc):
    opList = [
        OpDesc(opClass="MemRead", opLat=2),
        OpDesc(opClass="FloatMemRead", opLat=2),
    ]
    count = 3

class O3_ARM_Cortex_x4_Store(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite", opLat=2),
        OpDesc(opClass="FloatMemWrite", opLat=2),
    ]
    count = 3

# Functional Units for this CPU
class O3_ARM_Cortex_x4_FUP(FUPool):
    FUList = [
        O3_ARM_Cortex_x4_Simple_Int(),
        O3_ARM_Cortex_x4_Complex_Int(),
        O3_ARM_Cortex_x4_Load(),
        O3_ARM_Cortex_x4_Store(),
        O3_ARM_Cortex_x4_FP(),
        O3_ARM_Cortex_x3_SIMD(),
    ]

class O3_ARM_Cortex_x4_BTB(SimpleBTB):
    numEntries = 8192
    tagBits = 20
    associativity = 4
    instShiftAmt = 2
    btbReplPolicy = LRURP()
    btbIndexingPolicy = BTBSetAssociative(
        num_entries=Parent.numEntries,
        set_shift=Parent.instShiftAmt,
        assoc=Parent.associativity,
        tag_bits=Parent.tagBits,
    )

# Bi-Mode Branch Predictor
class O3_ARM_Cortex_x4_BP(BiModeBP):
    btb = O3_ARM_Cortex_x4_BTB()
    ras = ReturnAddrStack(numEntries=64)
    globalPredictorSize = 32768
    globalCtrBits = 2
    choicePredictorSize = 32768
    choiceCtrBits = 2
    instShiftAmt = 2
    # privatePredictorSize = 16384
    # privateCtrBits = 2

class O3_ARM_Cortex_x4(ArmO3CPU):
    LQEntries = 64
    SQEntries = 64
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
    fetchBufferSize = 64
    fetchToDecodeDelay = 3
    decodeWidth = 10
    decodeToRenameDelay = 1
    renameWidth = 10
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 10
    issueWidth = 10
    wbWidth = 10
    fuPool = O3_ARM_Cortex_x4_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 10
    squashWidth = 10
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    numPhysIntRegs = 192
    numPhysFloatRegs = 128
    numPhysVecRegs = 128
    numIQEntries = 192
    numROBEntries = 384

    switched_out = False
    branchPred = O3_ARM_Cortex_x4_BP()

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
class O3_ARM_Cortex_x4_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 8
    size = "64KiB"
    assoc = 4
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True

# Data Cache
class O3_ARM_Cortex_x4_DCache(Cache):
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 10
    tgts_per_mshr = 16
    size = "64KiB"
    assoc = 4
    write_buffers = 16
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True

# L2 Cache
class O3_ARM_Cortex_x4L2(Cache):
    tag_latency = 12
    data_latency = 12
    response_latency = 12
    mshrs = 24
    tgts_per_mshr = 16
    size = "8MiB"
    assoc = 8
    write_buffers = 8
    clusivity = "mostly_excl"
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency=1, prefetch_on_access=True)
    tags = BaseSetAssoc()
    replacement_policy = LRURP()

class O3_ARM_Cortex_x4_L3(Cache):
    size = "32MiB"
    assoc = 16
    tag_latency = 7
    data_latency = 7
    response_latency = 7
    mshrs = 20
    tgts_per_mshr = 12
    write_buffers = 16
    clusivity = "mostly_excl"

# MMU配置
class O3_ARM_Cortex_x4_MMU:
    def __init__(self):
        # 指令TLB配置
        self.itb = ArmITB(
            size=48,
            assoc=3,
            is_stage2=False,
            lookup_latency=1,
            fill_latency=10,
            tlb_level=1
        )
        # 数据TLB配置
        self.dtb = ArmDTB(
            size=48,
            assoc=3,
            is_stage2=False,
            lookup_latency=1,
            fill_latency=10,
            tlb_level=1
        )
        # L2共享TLB配置
        self.l2_tlb = BaseTLB(
            size=2048,
            assoc=16,
            lookup_latency=2,
            fill_latency=20,
            tlb_level=2
        )