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
> If you are unfamiliar with the basic knowledge about RROS/Rust/Dual-kernel, you can do our [lab](https://github.com/rust-real-time-os/os_lab) first to learn them.

It is easy to contribute to RROS. Any improvement, such as bug/typo fix, code refactor, new feature, performance evalute/improvement, realtime program migration, and board adaptive is welcome! The basic follow is as follows:
- (Option)Learn the basic knowledge about RROS(you can find that in our Lab).
- Read the tutorial to clone the data and run RROS.
- Follow the [steps](#contribute-steps) below to make your change.
- Contribute the code in the right [format](#submission-format).

## Contribute steps

1. You can either find the tasks by yourself or start with one of the [first good issues]().
2. Claim the task if there is already an issue. If not, create a corresponding issue and  explaining the task background; if it is a bug discovered by yourself, you also need to create an issue before submitting the code.
3. Complete the development and submit the code in the form of a PR, and pass the CI test on GitHub;
4. Modify the code based on the opinions and feedback of reviewers until it is merged, and then every PR merge requires approval from the maintainer of this subsystem.  PR needs to be merged in rebase format, without intermediate merge commits.
5. If you have any questions about the subsystem, you can find the corresponding maintainers in [here](https://rust-real-time-os.github.io/website/docs/contributing/maintainers).

## Submission format

1. First, the format of the commit title should be as follows: `language: subsystem: content`
  - Language: rust/c:
  - Subsystem: the involved subsystem;
  - Content: the main content of this modification;
    - If it is a bug fix, it should be: fix the bug of ......
    - If it is a feature, it needs to specifically indicate the content of the feature
    - If it is a round patch, it needs to specify the range of the round patch. The round patch cannot be included in a large commit; keep the shape of the original commit
2. The commit message needs to specifically describe the content of this modification
  - If it is a commit related to functionality, describe adding the feature or modifying the specific content of the feature
  - If it is a bug fix commit, explain the cause of the bug and how it was fixed in the bug fix
3. Add an issue link on a separate line in the commit message for each one to facilitate traceability
4.  Note:
  -  Chinese text should not be included in the commit message
  -  If use English colons, add a space after them
5.  A PR commit Example:
    ```
      Title
      rust: factory: add the oob_write syscall

      Message
      The oob_write syscall is one of the three syscalls in rros. Each factory 
      implements the oob_write file ops and has different commands according to the 
      arguments of this syscall.

      https://github_issue_link
    ```
