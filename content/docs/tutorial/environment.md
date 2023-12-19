---
title: "Setup the Environment"
description: "how to setup the environment"
summary: ""
date: 2023-11-25T13:48:54+08:00
lastmod: 2023-11-25T13:48:54+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "example-e46e39178633b3dd51aea8e870e3a562"
weight: 50
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

You can have the environment either with docker or build yourself.

## Docker

1. Install docker and pull the code

Docker can be installed directly on windows/linux/mac, mainly refer to [official documentation](https://docs.docker.com/desktop/), the specific steps are as follows:

- Install on windows
  - Download [docker desktop](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe) and click install.
  - After installing docker, if you are prompted that wsl2 is not installed and cannot be started normally, this is because using docker on windows requires turning on wsl2 or hyper-v related components. Here we use wsl2, this part of the content refers to Microsoft's [official instructions](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package).
    - Open PowerShell as an administrator ("Start" menu > "PowerShell" > right-click > "Run as administrator"), and then enter the following command:
      ```powershell
      dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
      dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
      ```
    - Download [wsl update package](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) and install it.
  - Restart the computer and start docker desktop, you can start it normally
    ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118024109.png)
- Install on linux ubuntu/mac
- Here, considering that there may be no graphical interface when installing on linux, the following command is used to explain
- The principle of running docker on linux is to use kvm virtualization technology. You can use the following command to detect whether linux meets the conditions of docker
  ```bash
  lsmod | grep kvm
  ```
  The correct output is as follows:
  ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118030849.png)
- Change the source of linux software package installation address
  ``` bash
   sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt-get update
   ```
   If the source is not changed successfully and GPG error occurs, you can refer to this [tutorial](https://askubuntu.com/questions/13065/how-do-i-fix-the-gpg-error-no-pubkey).
- Install docker
- ```bash
  sudo apt-get install docker-ce
  ```
- Docker source change
  ```bash
   vim /etc/docker/daemon.json
   # Add the following content
   # {
   #   "registry-mirrors": ["https://akchsmlh.mirror.aliyuncs.com"]
   # }    
   ```
- Check if it can be executed normally
- ``` bash
  docker run hello-world
  ```
  ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230310190412.png)

2. After the installation is complete, we provide two ways to obtain the docker image that owns the environment.
   - Open the command line window, use the `docker pull TODO:[add a docker image link] ` command to pull the rros docker image. Then use `docker run -itd --security-opt seccomp=unconfined --name rros_dev TODO:[add a docker image link] /bin/bash` to run a container named rros_lab.
   - Use the [Dockerfile](#Dockerfile) that we provide. Copy the content of [Dockerfile](#Dockerfile) to file named `Dockerfile` on your project path, use the `docker build -t rros .` command to build the rros docker image. Then use `docker run -itd --security-opt seccomp=unconfined --name rros_dev rros /bin/bash`

3. Finally, we use vscode to complete the subsequent experiments.
- If your docker is running on your local machine, not a remote Linux server, just install the `dev-container` plug-in in the vscode application market:
  ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230223105223.png)
- Click the plug-in, and we can see the docker we started, and then click `Attach in New Window` to enter our docker
- Then open the folder of our project in the container
  ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118033949.png)
- Enter `/data/bupt-rtos/rros`
- ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230223101753.png)


> - If your docker is running on a remote Linux server, you need to install the `remote-ssh` plug-in
>   ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118032735.png)
> - You need to configure ssh first
> - ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118033530.png)
> - Replace the `ip_address` in the figure with the ip address of the Linux server, set `ssh_port` to the corresponding ssh service port (usually 22), and replace `user_name` with the user name of the Linux server
> - ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118033325.png)
> - Finally open the configured remote server, and then the steps are the same as opening the docker container locally in vscode
> - ![](https://raw.githubusercontent.com/Richardhongyu/pic/main/20230118033629.png)
> - If you find that there is no container information after opening the plug-in, it may be because the account used does not have docker permissions. Find the docker user group in /etc/group and add your own user name.


## local

If you enjoy the fun of configuration everything by yourself, you can also build your development environment.

This document describes how to set up the development environment for RROS, including the installation of the compilation toolchain, development tools, QEMU emulator, and debugging tools. If you encounter problems, refer to the appendix for potential solutions.

### Requirements: Build
This section covers the installation of the compilation toolchain.

#### Rust Toolchain
1. **Install Rust-related Tools**:
   - If `rustup`, `rustc`, `cargo` are already installed, skip this step.
   - Use `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` to install.
   - If you encounter network issues, visit https://sh.rustup.rs for the shell script or choose the appropriate `rust-init.sh` script from Other Installation Methods - Rust Forge.
   - Check installation success with `rustup --version` and `cargo --version`.

2. **Install Rust Toolchain**:
   - Install a specific version of the `rustc` compiler as new versions might not work due to reliance on unstable Rust features for kernel compilation.
   - Use `rustup toolchain install beta-2021-06-23-x86_64-unknown-linux-gnu`.
   - In the RROS root directory, set the specific Rust toolchain version with `rustup override set beta-2021-06-23-x86_64-unknown-linux-gnu`.

3. **Install Rust Standard Library Source**:
   - Necessary for cross-compiling core and alloc.
   - In the RROS root directory, execute `rustup component add rust-src`.

#### LLVM Toolchain
- **LLVM Version**:
  - Use LLVM-13 as LLVM-16 and LLVM-14 have compatibility issues with bindgen v0.56.0.
- **Installation Methods**:
  - **Binary Installation**: Download the binary package from the LLVM GitHub releases page.
  - **Source Installation**: Requires `cmake`. Download the source code and compile it. Note that compiling LLVM requires significant memory.
  - **Official Script Installation**: Use the script from the LLVM website, but it demands a stable network connection.
- **Install libtinfo.so.5** for clang-13 compatibility.

#### Bindgen
- Install bindgen for generating Rust code from C code in the kernel.
- Use `cargo install --locked --version 0.56.0 bindgen` and check with `bindgen --version`.

#### GCC/G++
- Install `g++` and `aarch64-linux-gnu-g++` cross-compilation tools.

#### Bison
- Check with `bison --version` and install if necessary.

### Requirements: Develop
- **Rustfmt, Clippy, Cargo, Rustdoc**: Automatically installed with the Rust toolchain.
- **Rust Analyzer**: Install via VSCode plugin. For non-cargo projects like RROS, create a `rust-project.json` file.

### Requirements: QEMU
- Install QEMU related tools with `apt-get install qemu qemu-system qemu-user`.
- Check the version with `qemu-system-aarch64 --version`.

### Requirements: Debug
- Use `gdb-multiarch` for ARM64 simulation environments.

### Requirements: Config
- Set environment variables `ARCH=arm64` and `CROSS_COMPILE=aarch64-linux-gnu-`.
- Configure Kconfig in the RROS root directory.

### Build & Run
- Compile RROS with `make LLVM=1 -j20`.
- Run and debug with QEMU using appropriate commands.

### Appendix
- **Command Not Found After Restart**: Likely due to not writing `export` commands in `.bashrc`.
- **Compilation Errors**: Try installing the required packages with `apt-get install`.

**Note**: If setting up the environment on a server, it's crucial to use Docker and avoid using `apt` directly on the server.

<h3 id="Dockerfile"> Dockerfile </h3>

```dockerfile
FROM ubuntu:22.04

LABEL maintainer="shanmu"
LABEL e-mail="syx@bupt.edu.cn"

WORKDIR /root

## install basic tools or libs: git, gdb, ssh, curl, xz-utils, bzip2, libtinfo5, cmake, cpio, vim
RUN apt-get update && apt-get upgrade -y \
    && apt install git -y \
    && apt-get install gdb-multiarch -y\
    && apt-get install openssh-server -y \
    && apt-get install curl -y \
    && apt-get install xz-utils -y \
    && apt-get install bzip2 -y \
    && apt-get install libtinfo5 -y \
    && apt-get install cmake -y \
    && apt-get install cpio -y \
    && apt-get install vim -y

## install qemu
RUN apt-get install qemu qemu-system qemu-user -y

## add env config
ENV ARCH=arm64 \
    CROSS_COMPILE=aarch64-linux-gnu-

## get RROS source and libevl source
RUN git clone https://github.com/BUPT-OS/RROS.git \
    && git clone https://github.com/BUPT-OS/libevl.git

## install compile toolchain
## 1. rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rust-init.sh \
    && chmod +x rust-init.sh \
    && sh rust-init.sh -y
ENV PATH /root/.cargo/bin:$PATH
## 2. LLVM
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.1/clang+llvm-13.0.1-x86_64-linux-gnu-ubuntu-18.04.tar.xz \
    && tar xvf clang+llvm-13.0.1-x86_64-linux-gnu-ubuntu-18.04.tar.xz \
    && mv clang+llvm-13.0.1-x86_64-linux-gnu-ubuntu-18.04 llvm
ENV PATH /root/llvm/bin:$PATH
## 3. bindgen and specific rust toolchain
WORKDIR /root/RROS
    RUN rustup toolchain install beta-2021-06-23-x86_64-unknown-linux-gnu \
    && rustup override set beta-2021-06-23-x86_64-unknown-linux-gnu \
    && rustup component add rust-src \
    && cargo install --locked --version 0.56.0 bindgen \
## 4. aarch64 cross-compilation tool
    && apt-get install gcc-12-aarch64-linux-gnu -y \
    && mv /usr/bin/aarch64-linux-gnu-gcc-12 /usr/bin/aarch64-linux-gnu-gcc \
## 5. some missing libraries for 'make menuconfig'
    && apt-get install flex -y \
    && apt-get install bison -y \
    && apt-get install libncurses-dev -y \
## 6. some missing libs or headers for compiling the kernel
    && apt-get install libssl-dev -y \
    && apt-get install bc -y \
## 7. generate rros_defconfig to .config
    && make LLVM=1 rros_defconfig

## build a rootfs using busybox
WORKDIR /root
RUN wget https://www.busybox.net/downloads/busybox-1.36.1.tar.bz2 \
    && tar xvf busybox-1.36.1.tar.bz2 \
    && mkdir -p rootfs \
    && cd /root/busybox-1.36.1 \
    && make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig \
    && make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- install CONFIG_PREFIX=/root/rootfs \
## change path to /root/rootfs, to construct a toy rootfs
    && cd /root/rootfs \
    && mkdir -p lib && cp /usr/aarch64-linux-gnu/lib/* lib/ && ln -s lib lib64 \
    && mkdir dev proc mnt sys tmp root \
    && echo '/bin/mount -t devtmpfs devtmpfs /dev' >> init \
    && echo 'exec 0</dev/console' >> init \
    && echo 'exec 1>/dev/console' >> init \
    echo 'exec 2>/dev/console' >> init \
    echo 'exec /sbin/init "$@"' >> init \
    && mkdir etc && mkdir etc/init.d \
    && echo 'PATH=/sbin:/bin:/usr/sbin:/usr/bin' >> etc/init.d/rcS\
    && echo 'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib:/usr/lib' >> etc/init.d/rcS \
    && echo 'export PATH LD_LIBRARY_PATH runlevel' >> etc/init.d/rcS \
    && echo '/bin/hostname root' >> etc/init.d/rcS \
    && echo 'mount -a' >> etc/init.d/rcS \
    && echo 'mkdir /dev/pts' >> etc/init.d/rcS \
    && echo 'mount -t devpts devpts /dev/pts' >> etc/init.d/rcS \
    && echo '/sbin/mdev > /proc/sys/kernel/hotplug' >> etc/init.d/rcS \
    && echo 'mdev -s' >> etc/init.d/rcS \
    && chmod +x etc/init.d/rcS \
    && echo 'proc    /proc   proc    defaults 0 0' >> etc/fstab \
    && echo 'tmpfs   /tmp    tmpfs   defaults 0 0' >> etc/fstab \
    && echo 'sysfs   /sys    sysfs   defaults 0 0' >> etc/fstab \
    && echo 'tmpfs   /dev    tmpfs   defaults 0 0' >> etc/fstab \
    && echo '::sysinit:/etc/init.d/rcS' >> etc/inittab\
    && echo 'console::askfirst:-/bin/sh' >> etc/inittab\
    && echo '::restart:/sbin/init' >> etc/inittab\
    && echo '::ctrlaltdel:/sbin/reboot' >> etc/inittab\
    && echo '::shutdown:/bin/umount -a -r' >> etc/inittab\
    && echo '::shutdown:/sbin/swapoff -a' >> etc/inittab\
    && echo 'USER="`root`"' >> etc/profile\                                                      
    && echo 'LOGNAME=$USER' >> etc/profile\
    && echo 'HOSTNAME=`/bin/hostname`' >> etc/profile\
    && echo 'HOME=/root' >> etc/profile\
    && echo 'PS1="[$USER@$HOSTNAME \W]\# "' >> etc/profile\
    && echo 'PATH=$PATH' >> etc/profile\
    && echo 'export USER LOGNAME HOSTNAME HOME PS1 PATH PATH LD_LIBRARY_PATH' >> etc/profile\
    && find ./* | cpio -H newc -o > rootfs.cpio \
    && gzip rootfs.cpio \
    && cp rootfs.cpio.gz /root/RROS/

## dirty clean
WORKDIR /root
RUN rm -rf busybox-1.36.1 busybox-1.36.1.tar.bz2 clang+llvm-13.0.1-x86_64-linux-gnu-ubuntu-18.04.tar.xz rust-init.sh
```

