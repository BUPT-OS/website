---
title: "Learn"
description: ""
summary: ""
date: 2023-12-08T00:10:22+08:00
lastmod: 2023-12-08T00:10:22+08:00
draft: true
menu:
  docs:
    parent: ""
    identifier: "learn-980c832450cda73d6234b212dfeed1ae"
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# Learn the kernel tools

Here are some guides about the tools we daily used in the kernel world.

## git

*In progress*

## qemu

### tutorial

TODO: add the vedio link

### snapshot

QEMU Snapshot Feature

Background:
The desire is for QEMU to have a snapshot feature, allowing the saving of the current state when a bug occurs. This snapshot can be accessed later for debugging purposes.

1. Creating a QCOW2 Image with qemu-img:
   - Use the command `qemu-img create -f qcow2 test.qcow2 32M` to create an image.
   - `test.qcow2` is the desired name for the image, and the size can be specified as needed, here it's set to 32M.
   - The common error "Error: No block device can accept snapshots" usually occurs due to the absence of an image.

2. Updating QEMU Command:
   - Modify the existing QEMU command by adding `-drive if=none,format=qcow2,file=test.qcow2`.

3. Saving a Snapshot:
   - To save a snapshot when a bug occurs or when needed, use Ctrl+A C to bring up the QEMU monitor, then use `savevm snapshot1` to save the snapshot, where `snapshot1` is the desired name for the snapshot.
   - Use `info snapshots` in the QEMU monitor to view all current snapshot information.

4. Loading a Snapshot and Debugging with GDB:
   - On top of the QEMU command with the `-drive` option, use the `-loadvm snapshot1` option to load the snapshot.
   - This can be combined with GDB for debugging.

## emails

Use `mutt` to send/recieve the mails and use `b4` to fetch the patches in the email list.

### mutt

Mutt is a simple command-line tool that can be used in conjunction with Git to send and reply to emails for community interactions. Its popularity is due to its straightforward configuration.

Here is a config file, you can put it in the `~/.muttrc` to configure you mutt.

```
# ================  SMTP  ====================
set smtp_url =  # smtp_url
set smtp_pass =  "" # your password here, find it in the email vendor
set ssl_force_tls = yes # Require encrypted connection

# ================  Composition  ====================
# set editor = vim
set edit_headers = yes  # See the headers when editing
set charset = UTF-8     # value of $LANG; also fallback for send_charset
# Sender, email address, and sign-off line must match
unset use_domain        # because joe@localhost is just embarrassing
set realname = "name" # Change this to your name
set from = "email" # Change this to your email
set use_from = yes

ignore *
unignore From: Date: To: Cc: Subject: Reply-To: List-ID: Message-ID: In-Reply-To:
hdr_order From: Date: To: Cc: Subject: Reply-To: List-ID: Message-ID: In-Reply-To:

set wrap=80
set text_flowed
set editor="vim -c 'set formatoptions+=w' -c 'set textwidth=72'"
```

> Tips:
> 1. When sending emails to the kernel community, keep in mind:
>   - Emails should not exceed 80 characters per line for easier reading.
>   - The format of the email should be plain text without any formatting. This is because reading formatted content requires additional email size, and command-line clients may not display rich text formats correctly.
>   - Use in-line replies instead of top replies.
> 2. It's advisable to cc (carbon copy) yourself when sending emails to the kernel community. This helps you better understand how your sent email looks and confirms its successful delivery.
> 3. Remember to include a reply when responding to emails.
> 4. If you encounter any problems, you can always ask the email system administrator for help.

### b4

Using b4 can quickly apply community patches to your Linux source code:

1. Install b4:
   - Run `pip3 install b4 --user` to install b4.

2. Obtain the patch:
   - Use `b4 am` or `b4 mbox` to get a patch. For example, you can run:
     `b4 am CANiq72nyTdfBQDrBNOV7MEhpbwM3hYEeyaVZgRpMv8xFkLBwdw@mail.gmail.com`

3. Merge the patch using git:
   - Use `git am` followed by the patch file, like `git am xx.mbox`, to merge the patch into your code.

