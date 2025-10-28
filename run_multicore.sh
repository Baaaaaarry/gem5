export IMAGE_PATH=/home/barry/wlk/gem5_arm_linux_images
export M5_PATH="/home/barry/wlk/gem5_arm_linux_images"

# 默认启动命令
./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

# 按照指定slice dump启动命令
./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

# slice dump + slice save ckpt
./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --save-slices --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

# 从保存的slice_id 断点启动
./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --restore-slice 6 --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

#taskset -c 0-1 ./geekbench_aarch64 --no-upload --multi-core --iterations 1 --skip-sysinfo --workload 201