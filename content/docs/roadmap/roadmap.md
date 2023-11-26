---
title: "Roadmap"
description: ""
summary: ""
date: 2023-11-26T21:31:49+08:00
lastmod: 2023-11-26T21:31:49+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "example-a133a08ae66364e55e783d7e8291de3b"
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

We plan to enhance RROS in the follow three aspects. 

## RROS kernel

- [ ] SMP ability of RROS kernel
  - Currently, RROS is capable of running in QEMU with smp. But there are still bugs running in the rpi4b.
- [ ] Performance measurement 
  - [ ] Latmus 
    - Latmus is still in developing.
  - [ ] Hestic
    - Hestic is still in developing.
- [ ] Unsafe eliminate
   - [ ] Use RFL interface rather than directly call bindgen the APIs
   - [ ] Rustify RROS by refactoring subsystems
- [ ] Catch up with linux-dovetial mainline and publish releases
  - RROS is pinned to Linux 5.13 for now. We plan to merge to the linux-dovetail mainline after most of the basic functions of RFL is merged into the linux-dovetail.


## Libevl compatibility

We plan to be compatible of the libevl interfaces and capable of running all of the libevl test programs.
As for now we support the r27 libevl and modify it temproraly to adjust RROS.

In the factories, we still have distence compared with evl.
Currently, we have already support the following test programs.
|program|State|
|--|--|
|proxy-echo|√|
|xbuf|√|
|||
|||

## Satellite scenerio enhancement

The satellite scenerio has high requirement in safety.
Thus, equipment RROS with abilities designed for the satellite is necessary.

- [ ] Fault tolerant in dual-kernel
  - There are bit flips in the space. If this happends in the key code seggment, it can cause computer to crash. 
  - Besides, Linux kernel maybe crash. We can not allow RROS to crash in this condition.
  - Thus, We need to enhance the fault tolerant ability in RROS. The aim to let RROS still be alive while Linux breaks.
- [ ] SMP enhancement
  - In the satellite, different sensors are connetced to OBC. If we want to replace radiation-enhanced OBC with a normal PC computer and move the computing ability of sensors to the OBC, the OBC must handle different tasks in the sametime.