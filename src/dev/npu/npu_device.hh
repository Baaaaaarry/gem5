/*
 * Minimal NPU device interface for gem5.
 *
 * This model is a thin stub that exposes an MMIO space and a DMA-capable
 * interface via DmaVirtDevice. It does not implement any real NPU
 * functionality and is intended only to validate integration paths.
 */

#ifndef __DEV_NPU_NPU_DEVICE_HH__
#define __DEV_NPU_NPU_DEVICE_HH__

#include "dev/dma_virt_device.hh"
#include "mem/translation_gen.hh"
#include "params/NPUDevice.hh"

namespace gem5
{

class NPUDevice : public DmaVirtDevice
{
  private:
    Addr pioAddr;
    Addr pioSize;
    Tick pioDelay;

    /**
     * Very simple translation generator that treats virtual addresses as
     * physical addresses (identity mapping). This is sufficient for a stub
     * model that does not rely on OS-managed virtual memory.
     */
    class IdentityTranslationGen : public TranslationGen
    {
      public:
        IdentityTranslationGen(Addr vaddr, Addr size)
          : TranslationGen(vaddr, size)
        {}

      private:
        void translate(Range &range) const override;
    };

  public:
    using Params = NPUDeviceParams;

    NPUDevice(const Params &p);

    /** MMIO read/write handlers. Currently they just acknowledge requests. */
    Tick read(PacketPtr pkt) override;
    Tick write(PacketPtr pkt) override;

    /** Address range exposed on the PIO bus. */
    AddrRangeList getAddrRanges() const override;

    /** DMA address translation helper. */
    TranslationGenPtr translate(Addr vaddr, Addr size) override;
};

} // namespace gem5

#endif // __DEV_NPU_NPU_DEVICE_HH__

