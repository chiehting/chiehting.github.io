---
date: 2025-07-16T15:07:51+08:00
updated: 2025-07-16T15:45:18+08:00
title: Unix 訊號定義
category: linux
tags:
  - unix
  - posix
type: note
post: true
---

在 unix 中的每個信號號都有對應的定義，決定了當進程接收到信號時的行為。下面表格中的 `Action` 列條目指定了每個信號的默認處置。

- Ign：Default action is to ignore the signal.
- Core：Default action is to terminate the process and dump core (see [core(5)](https://man7.org/linux/man-pages/man5/core.5.html)).
- Stop：Default action is to stop the process.
- Cont：Default action is to continue the process if it is currently stopped.

<!--more-->

### Refencers

https://man7.org/linux/man-pages/man7/signal.7.html

### Standard signals

| Signal    | Standard | Action | Comment                                                                    |
| --------- | -------- | ------ | -------------------------------------------------------------------------- |
| SIGABRT   | P1990    | Core   | Abort signal from abort(3)                                                 |
| SIGALRM   | P1990    | Term   | Timer signal from alarm(2)                                                 |
| SIGBUS    | P2001    | Core   | Bus error (bad memory access)                                              |
| SIGCHLD   | P1990    | Ign    | Child stopped or terminated                                                |
| SIGCLD    | -        | Ign    | A synonym for SIGCHLD                                                      |
| SIGCONT   | P1990    | Cont   | Continue if stopped                                                        |
| SIGEMT    | -        | Term   | Emulator trap                                                              |
| SIGFPE    | P1990    | Core   | Erroneous arithmetic operation                                             |
| SIGHUP    | P1990    | Term   | Hangup detected on controlling terminal<br>or death of controlling process |
| SIGILL    | P1990    | Core   | Illegal Instruction                                                        |
| SIGINFO   | -        |        | A synonym for SIGPWR                                                       |
| SIGINT    | P1990    | Term   | Interrupt from keyboard                                                    |
| SIGIO     | -        | Term   | I/O now possible (4.2BSD)                                                  |
| SIGIOT    | -        | Core   | IOT trap. A synonym for SIGABRT                                            |
| SIGKILL   | P1990    | Term   | Kill signal                                                                |
| SIGLOST   | -        | Term   | File lock lost (unused)                                                    |
| SIGPIPE   | P1990    | Term   | Broken pipe: write to pipe with no<br>readers; see pipe(7)                 |
| SIGPOLL   | P2001    | Term   | Pollable event (Sys V);<br>synonym for SIGIO                               |
| SIGPROF   | P2001    | Term   | Profiling timer expired                                                    |
| SIGPWR    | -        | Term   | Power failure (System V)                                                   |
| SIGQUIT   | P1990    | Core   | Quit from keyboard                                                         |
| SIGSEGV   | P1990    | Core   | Invalid memory reference                                                   |
| SIGSTKFLT | -        | Term   | Stack fault on coprocessor (unused)                                        |
| SIGSTOP   | P1990    | Stop   | Stop process                                                               |
| SIGTSTP   | P1990    | Stop   | Stop typed at terminal                                                     |
| SIGSYS    | P2001    | Core   | Bad system call (SVr4);<br>see also seccomp(2)                             |
| SIGTERM   | P1990    | Term   | Termination signal                                                         |
| SIGTRAP   | P2001    | Core   | Trace/breakpoint trap                                                      |
| SIGTTIN   | P1990    | Stop   | Terminal input for background process                                      |
| SIGTTOU   | P1990    | Stop   | Terminal output for background process                                     |
| SIGUNUSED | -        | Core   | Synonymous with SIGSYS                                                     |
| SIGURG    | P2001    | Ign    | Urgent condition on socket (4.2BSD)                                        |
| SIGUSR1   | P1990    | Term   | User-defined signal 1                                                      |
| SIGUSR2   | P1990    | Term   | User-defined signal 2                                                      |
| SIGVTALRM | P2001    | Term   | Virtual alarm clock (4.2BSD)                                               |
| SIGXCPU   | P2001    | Core   | CPU time limit exceeded (4.2BSD);<br>see setrlimit(2)                      |
| SIGXFSZ   | P2001    | Core   | File size limit exceeded (4.2BSD);<br>see setrlimit(2)                     | 
| SIGWINCH  | -        | Ign    | Window resize signal (4.3BSD, Sun)                                         |