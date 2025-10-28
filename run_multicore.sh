export IMAGE_PATH=/home/barry/wlk/gem5_arm_linux_images
export M5_PATH="/home/barry/wlk/gem5_arm_linux_images"
./build/ARM/gem5.opt configs/example/arm/arm_multicore_slc.py --slice-run --slice-ticks 10ms --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --cpu-type="x4a720"
#./build/ARM/gem5.fast configs/example/arm/arm_multicore_4@X4+4@A720.py --restore=./m5out/cpt.1349300388627 --disk=${IMAGE_PATH}/ubuntu-18.04-arm64-docker.img --kernel=${IMAGE_PATH}/../binaries/vmlinux.arm64 --caches --last-cache-level 3 --cpu-type="x4a720"

#taskset -c 0-1 ./geekbench_aarch64 --no-upload --multi-core --iterations 1 --skip-sysinfo --workload 201
