---
date: 2023-07-27T17:02:44+08:00
updated: 2023-08-17T14:50:44+08:00
title: Laravel 框架產生的 cookie XSRF-TOKEN 需不需要使用 HttpOnly
category: system-design
tags:
  - system-design
  - php
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: https://security.stackexchange.com/questions/175536/does-a-csrf-cookie-need-to-be-httponly
post: true
---

### Evergreen Note

Question :: Does a CSRF cookie need to be HttpOnly such as XSRF-TOKEN cookie from Laravel.

Answer :: CSRF cookie 可以不用使用 HttpOnly flag, 因為 HttpOnly flag 保護的前提下已經是被 XSS([[cross-site-scripting]]) 攻擊, 同域的狀況下 CSRF cookie 已經失去其保護作用. 而且 XSS is a much bigger hole than CSRF. 所以 Laravel 產生的 XSRF-TOKEN cookie 可以不使用 HttpOnly flag.

<!--more-->

### Summary

這篇再討論防止 Cross Site Request Forgery(CSRF) 使用的 cookie 需不需要使用 HttpOnly. 像是 Laravel 框架中的 XSRF-TOKEN. 要理解這個問題, 首先要先釐清 CSRF 與 Cookie HttpOnly 的作用.

CSRF 攻擊是惡意網站偽造我的網站並發送請求到我的服務, 一般情況下會透過用戶的瀏覽器發送請求, 所以儲存在用戶上的 cookie 也都會被帶上, 我的服務就會判定就是該用戶的請求. 而 CSRF token 則可以保護我的服務收到的請求都是同域, 因為跨域取不到 CSRF token.

Cookie 的 HttpOnly flag 其目的是防止 Javascript 可以讀寫 cookie, 透過禁用 `document.cookie` 的方式防止某些攻擊, 例如 Cross-Site Scripting(XSS) 攻擊時其更難執行. XSS 會注入攻擊碼至我的服務中, 使我的服務執行攻擊腳本, 進而對用戶造成傷害.

現在回到 XSRF-TOKEN 需不需要使用 HttpOnly. 由於 XSRF-TOKEN 是防止跨站攻擊,  HttpOnly flag  是 XSS 後防止 JS 竊取. 所以已經被 XSS 的話 XSRF-TOKEN 應該就失去保護之目的了, 因為是同域. 在被 XSS 的情況下, 攻擊者已經沒有竊取 XSRF-TOKEN 的必要, 因為每次請求用戶瀏覽器都會帶上; 攻擊者已經沒有改寫 XSRF-TOKEN 的必要, 因為改寫了用戶請求就會失敗. 所以 XSRF-TOKEN 可以不用 HttpOnly flag.

另外 [Laravel 文件](https://laravel.com/docs/10.x/csrf#csrf-x-xsrf-token) 也明確表明 XSRF-TOKEN 創建是為了給 JavaScript 框架或套件使用的, 用於在同域下設置表頭 X-XSRF-TOKEN, 所以理應要給 JavaScript 讀取. Laravel 框架下產生的 XSRF-TOKEN 可以不用 HttpOnly flag.

### Note

原文 :: [Does a CSRF cookie need to be HttpOnly?](https://security.stackexchange.com/questions/175536/does-a-csrf-cookie-need-to-be-httponly)

We were recently handed a security report containing the following:

>Cookie(s) without HttpOnly flag set

vulnerability, which we apparently had in one of our internal applications.

The applied fix was as simple as setting Django's [`CSRF_COOKIE_HTTPONLY` configuration parameter](https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-cookie-httponly) to `True`.

But, this is what got me confused. The Django documentation says:

>**<span style="background-color: #ffffcc; color: red">Designating the CSRF cookie as HttpOnly doesn’t offer any practical protection because CSRF is only to protect against cross-domain attacks.</span> If an attacker can read the cookie via JavaScript, they’re already on the same domain as far as the browser knows, so they can do anything they like anyway. (XSS is a much bigger hole than CSRF.)**
>
>Although the setting offers little practical benefit, it’s sometimes required by security auditors.

Does this mean that **<span style="background-color: #ffffcc; color: red">there is no actual vulnerability here</span> and we just have to be compliant with the security auditing rules**?

#### 97 樓

As [joe says](https://security.stackexchange.com/a/175538/98538), **there is no real security benefit to this**. It is pure security theater. I'd like to highlight this from [the documentation](https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-cookie-httponly):

> If you enable this and need to send the value of the CSRF token with an AJAX request, your JavaScript must pull the value from a hidden CSRF token form input on the page instead of from the cookie.

**The purpose of the HttpOnly flag is to make the value of the cookie unavailable from JavaScript, so that it can not be stolen if there is a XSS vulnerability. But the CSRF-token must somehow be available so it can be double submitted** - thats the whole point with it, after all. So Django solves this by including the value in a hidden form field. This negates the whole benefit of HttpOnly, since an attacker can just read the value of the form field instead of the cookie.

#### 18 樓

I think the main point of confusion here is that the Django docs are specifically talking about the *CSRF* use case for a cookie. **In order to understand why the `httpOnly` flag adds no value in preventing CSRF, you need to understand both CSRF and how cookies work.**

**<span style="background-color: #ffffcc; color: red">CSRF is when a 3rd party triggers your user's browser to make a request to your server, and their browser automatically sends your server's cookies along with the request, as expected</span>. What you don't want is for your server to interpret this request as actually coming from your user, so you use a [CSRF mitigation](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) technique.** The whole point of CSRF mitigation is **to be able to detect when the request didn't come from your own domain (i.e. from your user interacting with your application)**.

Briefly, how cookies work: **Whenever a user's browser sends a request to your domain/server, it automatically sends all the cookies associated with your domain, regardless of the `httpOnly` flag. Cookies therefore allow your client or your server to attach information to a user's browser that will be returned to your server automatically along with any follow-on requests. <span style="background-color: #ffffcc; color: red">Cookies with the `httpOnly` flag cannot be accessed from javascript.</span> They probably shouldn't be considered a secure place to store information, but they do provide the advertised functionality.**

Back to CSRF implemented using a cookie — <span style="background-color: #ffffcc; color: red">**in this case** the `httpOnly` flag is pointless</span> — <span style="background-color: #ffffcc; color: red">the crux of CSRF is that they don't need to read your user's cookies, they just need your user's browser to send the associated cookies to your server along with the network request they forced it to send.</span> The `httpOnly` flag, in general, does provide value in that it prevents client access to those cookies, and if your server returns any cookies, you should probably make them `httpOnly`. If you are using a cookie for CSRF, then, you shouldn't do that, and you should spend your time rethinking that rather than making it an `httpOnly` cookie. So, in general, it seems like that is a good rule of thumb — your server shouldn't send any non-`httpOnly` cookies unless it is specifically intended to be accessed by the client javascript.