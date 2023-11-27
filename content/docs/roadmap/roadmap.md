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

We aim to augment RROS across three distinct dimensions:

## RROS kernel

- [ ] SMP Enhancement
  - Presently, RROS demonstrates proficiency in executing within QEMU environments utilizing SMP. Nonetheless, anomalies persist when operating on the rpi4b platform.
- [ ] Benchmarking and Performance Analysis
  - [ ] Latmus Evolution
    - The development of Latmus remains an ongoing endeavor.
  - [ ] Hestic Maturation
    - Hestic continues its trajectory of refinement and development.
- [ ] Eradication of Unsafe Practices
   - [ ] Prioritize utilization of the RFL interface over direct invocations of bindgen APIs
   - [ ] Transform and elevate RROS through comprehensive subsystem refactoring, adhering to Rust paradigms
- [ ] Synchronizing with Linux-Dovetail’s Forefront and Release Dissemination
  - RROS is pinned to Linux 5.13 for now. We plan to merge to the linux-dovetail mainline after most of the basic functions of RFL are merged into the linux-dovetail.


## Libevl compatibility

Our objective encompasses attaining compatibility with libevl interfaces and ensuring full operability of all libevl diagnostic programs. Current developments have led to the provisional support of r27 libevl, with bespoke modifications catering to RROS requisites.

In the realm of `factory`, a discernible disparity with linux-evl remains. To date, the following test programs have been successfully integrated:
|program|State|
|--|--|
|proxy-echo|√|
|xbuf|√|
|||
|||

## Satellite Scenario Fortification

Given the stringent safety protocols inherent in satellite operations, it is imperative to endow RROS with features tailored for such environments.

- [ ] Fault-tolerant in dual-kernel
  - The occurrence of bit flips in space, particularly in vital code segments, can precipitate kernel malfunctions.
  - In the event of a Linux kernel failure, it is crucial to maintain RROS’s operational integrity.
  - The objective is to bolster RROS's resilience, ensuring its functionality in the face of Linux system failures.
- [ ] SMP Augmentation
  - Onboard satellite systems, especially those interfacing with diverse sensors, necessitate robust multitasking capabilities. The vision is to substitute radiation-hardened Onboard Computers (OBCs) with standard PCs, transferring sensor computation to these OBCs, thereby necessitating enhanced SMP capabilities within RROS.