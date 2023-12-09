---
title: "Quick Start"
description: ""
summary: ""
date: 2023-11-28T22:49:07+08:00
lastmod: 2023-11-28T22:49:07+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "quick-start-fa271bc29261e91a723726602a98661f"
weight: 60
toc: true
authors: ["qichen"]
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
## Boot the RROS on QEMU
On Linux (Debian-like distros), do the following:

1. Clone this repository:

   ```bash
   git clone https://github.com/BUPT-OS/RROS.git
   ```

2. Install Rust toolchain:

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   switch to `beta-2021-06-23-x86_64-unknown-linux-gnu`. Currently, we only support this compiler version.

   ```bash
   rustup toolchain install beta-2021-06-23-x86_64-unknown-linux-gnu
   ```

   Set the rust toolchain for this project:

   ```bash
   cd RROS
   rustup override set beta-2021-06-23-x86_64-unknown-linux-gnu
   ```

   Add the rust `no-std` component.

   ```bash
   rustup component add rust-src
   ```
   
3. Select compile options

   Create a default configuration:

   ```bash
   export CROSS_COMPILE=aarch64-linux-gnu-
   export ARCH=arm64

   make LLVM=1 defconfig
   make LLVM=1 menuconfig
   ```

   select the following options:

   ```
   General Setup --->  Rust Support
   Kernel Features ---> Bupt real-time core
   ```

   You might need to disable the option `Module versioning support` to enable `Rust support`:

   ```
   Enable loadable module support ---> Module versioning support.
   ```

4. Compile the kernel

   ```bash
   export CROSS_COMPILE=aarch64-linux-gnu-
   export ARCH=arm64
   make LLVM=1 -j
   ```

   If you want to boot on Raspberry PI 4, you need to generate dtbs and modules additionally.

   ```bash
   export INSTALL_MOD_PATH=/path/to/mod
   export INSTALL_DTBS_PATH=/path/to/dtbs
   make modules_install dtbs_install -j
   ```

   And move `broadcom`, `lib`, `overlays`, and `Image` to the boot partition of the SD card.

5. Run on simulator

   You need a filesystem to boot the kernel on QEMU. 

   Here's an example of how to run on QEMU:

   ```bash
   qemu-system-aarch64 -nographic  \
       -kernel Image \
       -drive file=ubuntu-20.04-server-cloudimg-arm64.img \
       -drive file=cloud_init.img,format=raw \
       -initrd ubuntu-20.04-server-cloudimg-arm64-initrd-generic \
       -machine virt-2.12,accel=kvm \
       -cpu host  -enable-kvm \
       -append "root=/dev/vda1 console=ttyAMA0"  \
       -device virtio-scsi-device \
       -smp 4 \
       -m 4096
   ```

## Run a real-time program on RROS

<style>
.responsive-video {
  width: 100%;
  height: auto;
}
</style>

<video class="responsive-video" controls>
  <source src="../demo.mp4" type="video/mp4" />

</video>

### prerequisite

Before you start, ensure your environment is adequately prepared. You will need:
* A compiled kernel image of RROS (located in arch/arm64/boot/Image)
* A filesystem (ramdisk or other Linux distribution filesystem)
* Compiled [libevl](https://github.com/BUPT-OS/libevl)

We have made modifications to libevl; compile it or download it from our [libevl release]().

You may need:
* QEMU (version 7.0+ for 9p filesystem usage)
TODO: add the requirements of RROS. 

If you don't have a proper environment, you can follow our [environment document](https://bupt-os.github.io/website/docs/tutorial/environment/).


### Write a Hello World program
You can choose either compile the program on host system or on the target system(RROS). In this tutorial, we provide a version
of cross compiling here.

Below is the Makefile. Essentially, it links your program with libevl. Update $LIBEVL to specify the location of libevl.

Notice we use `-static` here (due to incompatibility between the glibc version on our filesystem and the external glibc). Dynamic linking is possible, but remember to copy libevl to /lib in your filesystem.

```Makefile
# SPDX-License-Identifier: MIT

ARCH = arm64
CROSS_COMPILE   = aarch64-linux-gnu-
CC              = $(CROSS_COMPILE)gcc
CXX             = $(CROSS_COMPILE)g++
LD              = $(CROSS_COMPILE)ld
AR              = $(CROSS_COMPILE)ar

LIBEVL ?= /example/libevl

CFLAGS  =  -I.                    \
           -I$(LIBEVL)/include
LDFLAGS = $(LIBEVL)/lib/libevl-0.a -lrt -static
TARGETS = demo

all: $(TARGETS)

demo: demo.c
        $(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

clean :
        rm -f $(TARGETS)⏎
```

And then here comes the hello world program which using the mechanism of `proxy` in libevl and print the message to a file.

```C
/*
 * SPDX-License-Identifier: MIT
 */

#include <assert.h>
#include <errno.h>
#include <error.h>
#include <evl/proxy.h>
#include <evl/syscall.h>
#include <evl/thread.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define BUFFER_SIZE 1024

#define CHECK_RET(ret)                                                         \
  do {                                                                         \
    if (ret < 0) {                                                             \
      fprintf(stderr, "Error on line %d : %s\n", __LINE__, strerror(errno));   \
      exit(EXIT_FAILURE);                                                      \
    }                                                                          \
  } while (0)

int proxyfd;
const char *msg = "Hello World!\n";

int main(int argc, char *argv[]) {
  int fd;
  int tfd;

  fd = open("example.txt", O_CREAT | O_WRONLY, 0644);
  CHECK_RET(fd);
  proxyfd = evl_new_proxy(fd, BUFFER_SIZE, "Proxy example:%d", getpid());
  CHECK_RET(proxyfd);
  tfd = evl_attach_self("thread:%d", getpid());
  CHECK_RET(tfd);
  int ret = oob_write(proxyfd, msg, strlen(msg));
  CHECK_RET(ret);
  return 0;
}

```

The program is quite simple. First, the program initially creates a file named a `example.txt`. It then uses the `evl_new_proxy` interface to
allocate a new proxy buffer in RROS of size `BUFFER_SIZE`. After that, the program `attach_self` and the kernel creates a real-time thread for it.
At this point, it becomes a real-time program. For this reason, it is advisable to avoid standard Linux system calls like `read` or `write`, which could result in high latency, even when running at high priority. Instead, employ syscalls
like `oob_read` or `oob_write` for kernel communication. In this example, `oob_write` is used to transmit the message to `example.txt` via the proxy.

Put the source file and the Makefile at same directory and compile them by:
```
LIBEVL=/path/to/libevl make
```



### Run your program on RROS
To execute the program, first boot RROS using QEMU. An example script is as follows:
```bash
qemu-system-aarch64 -cpu cortex-a57 \
      -machine type=virt -nographic \
      -smp 4 -m 2048 \
      -kernel RROS/arch/arm64/boot/Image \
      -append "console=ttyAMA0 root=/dev/vda2 rw" \
      -drive if=none,file=raspios-bullseye-arm64.img,id=hd0,format=raw \
      -device virtio-blk-device,drive=hd0 \
      -virtfs local,path=/example,mount_tag=host0,security_model=passthrough,id=host0
```
Once the system is up and running, employ any preferred method to transfer the binary demo to the RROS filesystem.

For 9p usage, execute the following command in the RROS command line:
```bash
mount -t 9p -o trans=virtio,version=9p2000.L host0 /mnt/shared
```

Navigate to `/mnt/shared`, and copy the file to your desired location.

To run the program:
```bash
./demo
```

If everything works well, a new file named example.txt should appear in the same directory, containing the "`Hello World!`" message.

Congratulations! Should you wish to contribute to our system, the next `tutorial` chapter offers detailed instructions.