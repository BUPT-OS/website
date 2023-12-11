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
weight: 250
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

### Debug in the qemu

When debugging, you might need to lower the compilation level. The provided `.config` file should already be configured for this, but if not, you can manually configure it.

#### Entering `menuconfig`

#### GDB Setup
If you encounter issues, consider the following:

1. **Enlarge the Window**: Sometimes, the display issues can be resolved by simply increasing the window size.
2. **Check Bash Environment Variables**: Ensure `$CROSS_COMPILE` and `$ARCH` are set. These should have been configured earlier.
   - Add to `~/.bashrc`:
     ```
     export CROSS_COMPILE=aarch64-linux-gnu-
     export ARCH=arm64
     ```
   - Set `kernel hacking > Rust Hacking > Optimization level > debug-level` to the lowest.

#### Using GDB for Remote Debugging
To debug the kernel, add `-s -S` to the kernel startup command (`-s` starts the gdb server, `-S` halts execution until `continue` is executed). For example:

```
qemu-system-aarch64 -nographic -kernel arch/arm64/boot/Image -initrd ../arm64_ramdisk/rootfs.cpio.gz -machine type=virt -cpu cortex-a57 -append "rdinit=/linuxrc console=ttyAMA0" -device virtio-scsi-device -smp 1 -m 4096 -s -S
```

Then, in a new window, start gdb (e.g., `rust-gdb`). In gdb, enter:

```
rust-gdb \
--tui vmlinux \
-ex "target remote localhost:1234" \
-ex "set architecture aarch64" \
-ex "set auto-load safe-path" \
-ex "set lang rust"
```

#### Setting Breakpoints in GDB
For example, to set a breakpoint at line 159 in `kernel/rros/init.rs`, use:

```
b kernel/rros/init.rs:159
```

Then start debugging with `continue`.

#### Common GDB Commands

| Command         | Function                                |
|-----------------|-----------------------------------------|
| `c`             | Continue to the next breakpoint         |
| `b filename:lineno` | Set a breakpoint at specified line    |
| `p variable`    | Print a variable                        |
| `x/`            | Print data at an address                |
| `finish`        | Jump to the end of the current function |
| `frame`         | View stack frame                        |
| `n`             | Next step, without entering functions  |
| `s`             | Step into, possibly entering functions |

#### VSCode Debugging
1. Start qemu in command line as shown above.
2. In the `.vscode` folder at the project root, open or create `launch.json` and paste the following configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "kernel-debug",
            "type": "cppdbg",
            "request": "launch",
            "miDebuggerServerAddress": "127.0.0.1:1234",
            "program": "${workspaceFolder}/vmlinux",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "logging": {
                "engineLogging": false
            },
            "MIMode": "gdb",
            "miDebuggerPath" : "/root/.cargo/bin/rust-gdb",
            "setupCommands": [
                {
                    "description": "set language rust",
                    "text": "set lang rust",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

Set breakpoints by clicking on the line number and start debugging with F5.

#### Using GDB Commands in VSCode
Enter GDB commands in the DEBUG CONSOLE with `-exec {gdb command}`.

### Appendix

#### Kernel Panic and Infinite Reboot
To disable this feature:

1. **Change QEMU Options**: Add `-no-reboot` to the QEMU run options.
2. **Modify Compilation Options**: In `make menuconfig`, under `Rust Hacking`, adjust `Panic timeout` to a higher number.

#### Analyzing Kernel Panic
1. **Using VSCode**: The debugger will stop at the error location during a panic.
2. **Using GDB or VSCode Debug Console**: Use `info symbol <address>` to find the symbol at a specific address.

This guide provides a comprehensive approach to debugging with GDB and VSCode, including setting up the environment, running QEMU for debugging, and analyzing kernel panics.

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
