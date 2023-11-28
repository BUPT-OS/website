---
title: "Contributing"
description: ""
summary: ""
date: 2023-11-25T19:37:00+08:00
lastmod: 2023-11-25T19:37:00+08:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "contributing-5910f6b8ad652b6c0cbe6834170989a4"
weight: 1
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

> **Before contributing**:
> If you are unfamiliar with RROS/Rust/Dual-kernel, we recommend embarking on our [lab](https://github.com/rust-real-time-os/os_lab) exercises as an introduction.

Contributing to RROS is a streamlined process. We welcome a wide spectrum of enhancements including, but not limited to, rectification of bugs or typographical errors, code refinement, introduction of novel features, performance optimization, migration of real-time programs, and board compatibility adjustments. The typical contribution workflow is outlined below:
- (Optional)Learn the basic knowledge about RROS(accessible in our Lab).
- Read the tutorial to clone the data and run RROS.
- Adhere to the [prescribed steps](#steps-for-contribution) to implement your modifications.
- Contribute the code in the [specified format](#format-for-submissions).

## Steps for Contribution

1. You can find the tasks by yourself or start with one of the [first good issues]().
2. Claim the task if there is already an issue. Otherwise, create a new issue detailing the task background; for self-identified bugs, an issue must precede the code submission.
3. Fulfill the development criteria, submit your code via a Pull Request (PR), and ensure it passes the GitHub Continuous Integration (CI) tests.
4. Revise your submission based on reviewer feedback until its incorporated. Note that every PR merge demands approval from the respective subsystem's maintainer. When you address the concerns, do not add a new commit. Just replace reset the old commits, add new commits and push force your original patches. PRs should be merged in rebase format, eschewing intermediate merge commits.
5. If you have any questions about the subsystem, you can find the relevant maintainers [here](https://rust-real-time-os.github.io/website/docs/contributing/maintainers).

## Format for Submissions

1. First, the format of the commit title should be as follows: `language: subsystem: content`
  - Language: rust/c:
  - Subsystem: the involved subsystem;
  - Content: a succinct description of the modification;
    - For bug fix, it should be: fix the bug of ......
    - For new features, clearly delineate the feature's attributes.
    - For patch issues, it needs to specify the range of the round patch. The round patch cannot be included in a large commit; keep the shape of the original commit
2. The commit message must thoroughly describe the content of this modification
  - For functionality-related commits: outline the added feature or the specific alterations made.
  - For bug fix commits: elucidate the bug's origin and the methodology of its resolution.
3. Add an issue link on a separate line in the commit message for each one to facilitate traceability
4. Additional Note:
  -  Refrain from including Chinese text in the commit message.
  -  If using English colons, add a space after them
  -  Does not forget to add "Signed-off-by sign" in the git commit message.
5.  A PR commit Example:
    ```
      Title
      rust: factory: add the oob_write syscall

      Message
      The oob_write syscall is one of the three syscalls in RROS. Each factory 
      implements the oob_write file ops and has different commands according to the 
      arguments of this syscall.

      https://github_issue_link

      Signed-off-by: 
    ```
