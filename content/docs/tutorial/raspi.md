---
title: "Raspi"
description: ""
summary: ""
date: 2023-12-08T00:34:39+08:00
lastmod: 2023-12-08T00:34:39+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "raspi-908fc5d02cad5f066f8452c926ba3e49"
weight: 200
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# Deploy RROS on the raspi

> Check whether you have these hardwares before getting start.
> Hardware Requirements:
> - Raspberry Pi (the model used here is 4B)
> - Raspberry Pi power supply
> - Micro HDMI to HDMI cable
> - A screen with HDMI interface
> - Mouse
> - Keyboard
> - SD card
> - SD card reader

## Burning the Raspberry Pi System:

1. **Download Raspberry Pi Imager**:
   - Visit the official Raspberry Pi website and download the Raspberry Pi Imager.

2. **Write the OS to the SD Card**:
   - Insert the SD card into your computer using the SD card reader.
   - Open Raspberry Pi Imager and select the Raspberry Pi OS (64-bit version) for writing.
   - Follow the instructions to write the OS onto the SD card.
   - Once the writing process is complete, safely eject the SD card reader from your computer.

3. **Setting Up the Raspberry Pi**:
   - Insert the SD card into the Raspberry Pi.
   - Connect the mouse and keyboard.
   - Connect the Raspberry Pi to a monitor using the micro HDMI to HDMI cable.
   - Power on the Raspberry Pi.
   - The first boot might take longer than usual, so be patient.
   - Once booted, go through the basic setup process, which includes configuring the network, setting a password, etc.
   - Remember to switch to the Tsinghua University mirror source for better performance in China.

This setup will get your Raspberry Pi up and running with the necessary hardware and software configurations.

## Compiling and Using RROS on Raspberry Pi

1. **Compile and Update RROS Kernel in a Container**:
   - Set up Docker container network penetration using VSCode and install `openssh-server`.
   - Compile the kernel and modules in the `linux-dovetail-v5.13-dovetail-rebase` directory. Check for successful compilation and then execute `./copy_to_raspberry.sh`.

   <!-- ![Alt text](https://bupt-os.github.io/website/architecture.png/raspi1.png)

   ![Alt text](https://bupt-os.github.io/website/architecture.png/raspi2.png) -->

2. **Transfer to Local Machine**:
   - Use `scp` to transfer files like `modules.tar.bz2`, `dtb.tar.bz2`, `Image`, and `overlays.tar.bz2` from the container to your local machine.

    ```bash
      #execute in your local machine
      scp root@localhost:/data/bupt-rtos/modules.tar.bz2 ./
      scp root@localhost:/data/bupt-rtos/dtb.tar.bz2 ./
      scp root@localhost:/data/bupt-rtos/Image ./
      scp root@localhost:/data/bupt-rtos/overlays.tar.bz2 ./
    ```

3. **Transfer to Raspberry Pi**:
   - Ensure the local machine and Raspberry Pi are on the same network.
   - Use `scp` to transfer the files to the Raspberry Pi.

    ```bash
      #transmiss to yout raspi
      scp .\Image  rtos@192.168.200.16:/home/rtos/
      scp .\dtb.tar.bz2  rtos@192.168.200.16:/home/rtos/
      scp .\modules.tar.bz2  rtos@192.168.200.16:/home/rtos/
      scp .\overlays.tar.bz2  rtos@192.168.200.16:/home/rtos/
    ```

4. **Unpack and Reboot on Raspberry Pi**:
   - On the Raspberry Pi, in the `/home/rtos` directory, run the `untar_modules.sh` script to move and extract the necessary files.

    ```bash
      #!/bin/bash

      sudo mv Image /boot/rros.img

      rm -fr modules
      tar -xvf modules.tar.bz2 modules
      sudo cp -r modules/lib/modules/* /lib/modules/

      rm -fr overlays
      tar -xvf overlays.tar.bz2 overlays
      sudo cp -r overlays/* /boot/overlays/

      rm -fr dtb.tar boot_dtb
      bunzip2 dtb.tar.bz2
      tar -xvf dtb.tar
      sudo cp -r boot_dtb/* /boot/
    ```

   - Add `kernel=rros.img` to `/boot/config.txt`.
   - Reboot the Raspberry Pi (if it fails, try a power cycle).

This process outlines the steps for compiling and deploying the RROS on a Raspberry Pi, including setting up the development environment, compiling the kernel, and transferring and installing the necessary files on the Raspberry Pi.