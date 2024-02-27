---
date: 2024-02-16T11:28:57+08:00
updated: 2024-02-20T17:19:22+08:00
title: rfc6265
category: internet
tags:
  - internet
  - ietf
  - rfc
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: https://www.rfc-editor.org/info/rfc6265
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 文章主要在研究 RFC 6265 - HTTP State Management Mechanism。文章是在定義 HTTP Cookie and Set-Cookie header fields 規範。

<!--more-->

### Summary

RFC 6265 - HTTP State Management Mechanism 是在定義 HTTP Cookies and Set-Cookie header fields。Cookie 是 Server / Client 資料交互的方法之一，是 developers of cookie-
generating servers 和 developers of cookie-consuming user agents 需要關心的重要議題。

第四章節在說明 Set-Cookie header fields 規範以及重要屬性 ([[internet-rfc-6265-server-requirements]])。

### Note

原文 :: [rfc6265](https://www.rfc-editor.org/info/rfc6265)

#### Abstract

<span style="background-color: #ffffcc; color: red">This document defines the HTTP Cookie and Set-Cookie header fields. These header fields can be used by HTTP servers to store state (called cookies) at HTTP user agents, letting the servers maintain a stateful session over the mostly stateless HTTP protocol.</span> Although cookies have many historical infelicities that degrade their security and privacy, the Cookie and Set-Cookie header fields are widely used on the Internet. This document obsoletes RFC 2965. [STANDARDS-TRACK]

Table of Contents

```text
1. Introduction
2. Conventions
   2.1. Conformance Criteria
   2.2. Syntax Notation
   2.3. Terminology
3. Overview
   3.1. Examples
4. Server Requirements
   4.1. Set-Cookie
        4.1.1. Syntax
        4.1.2. Semantics (Non-Normative)
   4.2. Cookie
        4.2.1. Syntax
        4.2.2. Semantics
5. User Agent Requirements
   5.1. Subcomponent Algorithms
        5.1.1. Dates
        5.1.2. Canonicalized Host Names
        5.1.3. Domain Matching
        5.1.4. Paths and Path-Match
   5.2. The Set-Cookie Header
        5.2.1. The Expires Attribute
        5.2.2. The Max-Age Attribute
        5.2.3. The Domain Attribute
        5.2.4. The Path Attribute
        5.2.5. The Secure Attribute
        5.2.6. The HttpOnly Attribute
   5.3. Storage Model
   5.4. The Cookie Header
6. Implementation Considerations
   6.1. Limits
   6.2. Application Programming Interfaces
   6.3. IDNA Dependency and Migration
7. Privacy Considerations
   7.1. Third-Party Cookies
   7.2. User Controls
   7.3. Expiration Dates
8. Security Considerations
   8.1. Overview
   8.2. Ambient Authority
   8.3. Clear Text
   8.4. Session Identifiers
   8.5. Weak Confidentiality
   8.6. Weak Integrity
   8.7. Reliance on DNS
9. IANA Considerations
   9.1. Cookie
   9.2. Set-Cookie
   9.3. Cookie2
   9.4. Set-Cookie2
10. References
   10.1. Normative References
   10.2. Informative References
Appendix A. Acknowledgements
```

#### Introduction

This document defines the HTTP Cookie and Set-Cookie header fields.
<span style="background-color: #ffffcc; color: red">Using the Set-Cookie header field, an HTTP server can pass name/value
pairs and associated metadata (called cookies) to a user agent. When
the user agent makes subsequent requests to the server, the user
agent uses the metadata and other information to determine whether to
return the name/value pairs in the Cookie header.</span>

<span style="background-color: #ffffcc; color: red">Although simple on their surface, cookies have a number of
complexities.  For example, the server indicates a scope for each
cookie when sending it to the user agent.  The scope indicates the
maximum amount of time in which the user agent should return the
cookie, the servers to which the user agent should return the cookie,
and the URI schemes for which the cookie is applicable.</span>

<span style="background-color: #ffffcc; color: red">For historical reasons, cookies contain a number of security and
privacy infelicities.  For example, a server can indicate that a
given cookie is intended for "secure" connections, but the Secure
attribute does not provide integrity in the presence of an active
network attacker.  Similarly, cookies for a given host are shared
across all the ports on that host, even though the usual "same-origin
policy" used by web browsers isolates content retrieved via different
ports.</span>

<span style="background-color: #ffffcc; color: red">There are two audiences for this specification: developers of cookie-
generating servers and developers of cookie-consuming user agents.</span>

To maximize interoperability with user agents, servers SHOULD limit
themselves to the well-behaved profile defined in Section 4 when
generating cookies.

User agents MUST implement the more liberal processing rules defined
in Section 5, in order to maximize interoperability with existing
servers that do not conform to the well-behaved profile defined in
Section 4.

This document specifies the syntax and semantics of these headers as
they are actually used on the Internet.  In particular, this document
does not create new syntax or semantics beyond those in use today.
The recommendations for cookie generation provided in Section 4
represent a preferred subset of current server behavior, and even the
more liberal cookie processing algorithm provided in Section 5 does
not recommend all of the syntactic and semantic variations in use
today.  Where some existing software differs from the recommended
protocol in significant ways, the document contains a note explaining
the difference.
