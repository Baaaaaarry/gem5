export IMAGE_PATH=/hdd_8T/barry/gem5_arm_linux_images
export M5_PATH="/hdd_8T/barry/gem5_arm_linux_images"

# 默认启动命令d9300，可对应修改d9300 -> d9200
./build/ARM/gem5.opt configs/example/arm/arm_multicore_d9200.py --cpu-type="D9200" --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/vmlinux.arm64 --bootscript configs/gemmini/fs-run.rcS --enable-gemmini --gemmini-cpu-idx 0 --gemmini-ctrl-addr 0x10030000 --gemmini-ctrl-size 0x1000 
#./build/ARM/gem5.opt configs/example/arm/arm_multicore_d9300.py --cpu-type="D9300" --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/vmlinux.arm64
# 按照指定slice dump启动命令
#./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"
#
# slice dump + slice save ckpt
#./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --save-slices --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

# 从保存的slice_id 断点启动
#./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --restore-slice 6 --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

#taskset -c 0 ./geekbench_aarch64 --no-upload --multi-core --iterations 1 --skip-sysinfo --workload 204
