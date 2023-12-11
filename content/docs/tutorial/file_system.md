---
title: "Choose a file System"
description: ""
summary: ""
date: 2023-12-08T00:09:26+08:00
lastmod: 2023-12-08T00:09:26+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "file-cd902c4c4d7402e2fd8c18a0c8ea2739"
weight: 150
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Background Knowledge

1. **File Formats Containing File Systems**:
   - `.cpio.gz`
   - `.img`
   - `.iso`

2. **File System Formats**:
   - ext4, ntfs, etc.

## Toy File System (Made with BusyBox)

1. **Using `.cpio.gz`**:
   - Utilize the minimal root directory from BusyBox.

## Using Mature File Systems

1. **Using `.img`**:
   - **Ubuntu-Raspberry Pi File System**:
     - `20-04-rootfs` is a folder containing the Ubuntu file system and should also have the EVL library.
     - To prepare the file system:
       ```
       rm rros.img 
       dd if=/dev/zero of=rros.img bs=1M count=2048
       mkfs.ext4 rros.img 
       mkdir rros-mount
       mount rros.img rros-mount/
       cp -rfp 20-04-rootfs/* rros-mount/
       umount rros-mount/
       e2fsck -f rros.img
       resize2fs -M rros.img 
       ```
   - **Raspberry Pi Official File System**:
     - Refer to https://www.mocusez.site/posts/98a4.html for guidance.

## File System Size Adjustment

1. **Expanding Raspberry Pi's QEMU File System**:
   - The Raspberry Pi file system is initially 4GB and needs to be expanded.
   - From the file system creation process, it's known that `qemu-img resize` can modify the size of an `.img` file. However, adjusting the size to 8GB previously did not work because it changed the entire disk size without recognizing the disk partition format. Therefore, the disk partition size needs to be rebuilt.
   - Following the steps from the file system creation process:
     - Skip the first two steps if you have already adjusted the size to 8GB with `qemu-size`.
     - Start directly from `fdisk /dev/vda2`.
     - Pay attention to the first sector, choosing 532480 (this number should be checked from the start area of `vda2`).
     - Note that references to `sda` in the blog should be changed to `vda`.

