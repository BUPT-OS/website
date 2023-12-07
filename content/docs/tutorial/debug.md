---
title: "Debug"
description: ""
summary: ""
date: 2023-12-08T01:41:49+08:00
lastmod: 2023-12-08T01:41:49+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "debug-4dbb806433bfd75e0e9242ef690b7f5a"
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# Debug RROS

### Debug in the qemu

*In progres*

### Debug in the raspi

1. **Hardware**:
   - Raspberry Pi 4B
   - J-Link V11
   - 8 Dupont lines (jumper wires)

2. **Configuration**:
   2.1 **Hardware Connection**:
      - To use the J-Link emulator with the Raspberry Pi, first connect the J-Link's JTAG interface to the Raspberry Pi's expansion board using Dupont lines. The Raspberry Pi's expansion interface already includes a JTAG interface. The J-Link emulator provides a 20-pin JTAG interface.
      - Connect 8 wires between the Raspberry Pi and the J-Link emulator as shown in the table (not displayed here).
      - Power up the Raspberry Pi and connect the J-Link's USB interface to the host computer.

   2.2 **Raspberry Pi Configuration**:
      - In `/boot/cmdline.txt`, add the parameters `rodata=off nosmp`. `rodata=off` makes the kernel code segment writable, which is necessary for setting software breakpoints during debugging. `nosmp` runs the kernel in single-core mode, as multi-core debugging is not yet perfected.
      - In `/boot/config.txt`, add the following parameters to enable the JTAG serial port and disable the default pull-down of GPIO pins:
        ```
        arm_64bit=1
        enable_uart=1
        enable_jtag_gpio=1
        gpio=22-27=np
        init_uart_clock=48000000
        init_uart_baud=115200
        ```

   2.3 **Host Debugging Machine Configuration**:
      - On Windows 11, use OpenOCD for debugging the Raspberry Pi. The connection is as follows: gdb → openocd → jlink → Raspberry Pi.
      - Install the libusb-winusb driver for connecting J-Link with OpenOCD on Windows (not required for Linux). Use Zadig from https://zadig.akeo.ie/ for this purpose.
      - If the J-Link is not recognized in the Device Manager, download a newer version of the J-Link software package from https://www.segger.com/downloads/jlink/.
      - Use Zadig to install the libusb-winusb driver for the J-Link device.

3. **Debugging**:
   - Install OpenOCD from https://gnutoolchains.com/arm-eabi/openocd/. 
   - Copy the `raspberrypi4.cfg` file from https://github.com/sysprogs/openocd/blob/master/tcl/target/raspberrypi4.cfg to the OpenOCD bin directory and modify it for debugging only CPU0.
   - Run OpenOCD with administrator privileges using the command: `openocd.exe -f ..\share\openocd\scripts\interface\jlink.cfg -f raspberrypi4.cfg`.
   - Open another command line, navigate to the kernel source folder, and run `gdb-multiarch --tui vmlinux`.
   - In GDB, connect to the target using `target extended-remote localhost:3333`.
   - You can now start normal debugging (refer to section 5 of "Using libevl for RROS testing" for further steps).
