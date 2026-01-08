/*
 * Minimal NPU device interface for gem5.
 *
 * This model is a thin stub that exposes an MMIO space and a DMA-capable
 * interface via DmaVirtDevice. It does not implement any real NPU
 * functionality and is intended only to validate integration paths.
 */

#include "dev/npu/npu_device.hh"

#include "base/addr_range.hh"
#include "base/logging.hh"
#include "base/trace.hh"
#include "debug/NPUDevice.hh"

namespace gem5
{

NPUDevice::NPUDevice(const Params &p)
  : DmaVirtDevice(p), pioAddr(p.pioAddr), pioSize(p.pioSize),
    pioDelay(p.pioDelay)
{
}

void
NPUDevice::IdentityTranslationGen::translate(Range &range) const
{
    // Identity mapping: treat vaddr as paddr.
    range.paddr = range.vaddr;
    // Use the full remaining size of the region.
    // range.size is already set by the TranslationGen base class.
}

Tick
NPUDevice::read(PacketPtr pkt)
{
    const Addr addr = pkt->getAddr();
    DPRINTF(NPUDevice, "MMIO read addr=%#x size=%u\n", addr, pkt->getSize());

    pkt->makeAtomicResponse();
    return pioDelay;
}

Tick
NPUDevice::write(PacketPtr pkt)
{
    const Addr addr = pkt->getAddr();
    DPRINTF(NPUDevice, "MMIO write addr=%#x size=%u\n", addr, pkt->getSize());

    pkt->makeAtomicResponse();
    return pioDelay;
}

AddrRangeList
NPUDevice::getAddrRanges() const
{
    AddrRangeList ranges;
    if (pioSize != 0) {
        ranges.push_back(RangeSize(pioAddr, pioSize));
    }
    return ranges;
}

TranslationGenPtr
NPUDevice::translate(Addr vaddr, Addr size)
{
    DPRINTF(NPUDevice, "DMA translate vaddr=%#x size=%u\n", vaddr, size);
    return TranslationGenPtr(new IdentityTranslationGen(vaddr, size));
}

} // namespace gem5

