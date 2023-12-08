---
title: "Introduction"
description: ""
summary: ""
date: 2023-11-28T16:59:49+08:00
lastmod: 2023-11-28T16:59:49+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "introduction-35d131bdc9d8bbb2e319772e07edfb5d"
weight: 50
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
RROS is a dual-kernel OS, consisting of a real-time kernel (in Rust) and a general-purpose kernel (Linux). RROS is compatible with almost all native Linux programs and offers real-time performance superior to RT-Linux. It is also being experimented with as the host OS for in-orbit satellites ([Tiansuan Project](http://www.tiansuan.org.cn/)).

The architecture shows as following:
<img src="../architecture.png" width="70%" height="50%">
