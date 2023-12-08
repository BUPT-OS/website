---
title: "environment"
description: "how to do"
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

# Environment

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

2. After the installation is complete, open the command line window, use the `docker pull TODO:[add a docker image link] ` command to pull the rros docker image. Then use `docker run -itd --security-opt seccomp=unconfined --name rros_dev TODO:[add a docker image link] /bin/bash` to run a container named rros_lab.

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

