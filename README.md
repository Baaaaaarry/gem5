# The gem5 Simulator

This git is forked from gem5, please see [gem5](./README_gem5.md) for more details.

## build

### prepare
```bash
# 1. git
sudo apt install git
# 2. gcc 10+, We support GCC Versions >=10, up to GCC 13
sudo apt install build-essential
# 3. SCons 3.0+
sudo apt install scons
# 4. Python 3.6+
sudo apt install python3-dev
# 5. protobuf 2.1+ (Optional)
sudo apt install libprotobuf-dev protobuf-compiler libgoogle-perftools-dev
# 6. Boost (Optional)
sudo apt install libboost-all-dev
```

### build gem5
```bash
# Arm opt (with debug feature)
python3 `which scons` build/ARM/gem5.opt -j9
# Arm fast (faster without debug feature)
python3 `which scons` build/ARM/gem5.fast -j9

# RISCV opt (with debug feature)
python3 `which scons` build/RISCV/gem5.opt -j9
# RISCV fast (faster without debug feature)
python3 `which scons` build/RISCV/gem5.fast -j9
```

| type  | description                                                                                                                                                                                                                                                                                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| debug | Built with no optimizations and debug symbols. This binary is useful when using a debugger to debug if the variables you need to view are optimized out in the opt version of gem5. Running with debug is slow compared to the other binaries.                                                                                                                            |
| opt   | This binary is build with most optimizations on (e.g., -O3), but with debug symbols included. This binary is much faster than debug, but still contains enough debug information to be able to debug most problems.                                                                                                                                                       |
| fast  | Built with all optimizations on (including link-time optimizations on supported platforms) and with no debug symbols. Additionally, any asserts are removed, but panics and fatals are still included. fast is the highest performing binary, and is much smaller than opt. However, fast is only appropriate when you feel that it is unlikely your code has major bugs. |

## Arm cortex simulator
### config
- [x2](configs/common/cores/arm/O3_ARM_Cortex_x2.py)
- [x3](configs/common/cores/arm/O3_ARM_Cortex_x3.py)
- [x4](configs/common/cores/arm/O3_ARM_Cortex_x4.py)

### download arm kernel and ramdisk

```bash
wget http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2
wget http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2

tar -xvjf aarch-system-20220707.tar.bz2
bunzip2 ubuntu-18.04-arm64-docker.img.bz2

ls
aarch-system-20220707.tar.bz2  binaries  disks  ubuntu-18.04-arm64-docker.img
```

### add custum bin to ramdisk
```bash
cd {path_to_gem5}
python3 ./util/gem5img.py mount {path_to_arm_linux_images}/ubuntu-18.04-arm64-docker.img {local_mount_point}

#copy bin into disk image
cp -r {custom_bin} {local_mount_point}/home

#unmonut disk image.
python3 ./util/gem5img.py umount {local_mount_point}
```

### run
```bash
export gem5_home={path_to_gem5}
export M5_PATH={path_to_arm_linux_images}

# start kernel with x2
$gem5_home/build/ARM/gem5.fast $gem5_home/configs/example/arm/starter_fs_x2.py --cpu="o3"  --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1

# start kernel with x3
$gem5_home/build/ARM/gem5.fast $gem5_home/configs/example/arm/starter_fs_x3.py --cpu="o3"  --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1

# start kernel with x4
$gem5_home/build/ARM/gem5.fast $gem5_home/configs/example/arm/starter_fs_x4.py --cpu="o3"  --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1

# term to kernel in another shell
$gem5_home/util/term/gem5term localhost 3456
```

## run with DDR
--mem-channels: memory channels
--mem-type: use "LPDDR5_8533_1x16_BG_BL32" for sim 8650 ddr

```bash
./build/ARM/gem5.fast configs/example/arm/starter_fs_x3.py --cpu="o3" --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1 --mem-channels=4 --mem-type="LPDDR5_8533_1x16_BG_BL32"
```

## Acceleration with checkpoint

```bash
# run atomic core to start kernel
$gem5_home/build/ARM/gem5.fast $gem5_home/configs/example/arm/starter_fs_x3.py --cpu="atomic"  --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1

# term to kernel
$gem5_home/util/term/gem5term localhost 3456

# save checkpoint
m5 checkpoint

# start O3 core to acceleration
# cpt.7368810596684 is the checkpoint file name in m5out folder
$gem5_home/build/ARM/gem5.fast $gem5_home/configs/example/arm/starter_fs_x3.py --restore=$gem5_home/m5out/cpt.7368810596684 --cpu="o3"  --num-cores=1 --disk-image=${M5_PATH}/ubuntu-18.04-arm64-docker.img --root-device=/dev/vda1
```
## BUGFIX LIST
1、增加定时保存和恢复断点功能：7431c4bb836bc9c2d224fae5d211017bda52233b
2、多核一致性实现按照CHI协议修改：2fe92e4c477e07bcb9957fee2aa3859177377abc
3、总线配置修改：b20b8601d9407b6ced071b846252f52ecdff1a9e
4、CoherentXBar Latency设置不合理导致启动挂死问题修复：1d1312954ef0d086ae17218a8c68979d00604afa
