---
title: Keycloak 26.7.1 Evaluate 的 Access Token aud 狀態
source: keycloak_實測
author:
  - chiehting
published: 2026-08-11
created: 2026-08-11
description: Keycloak Evaluate 的 audience 驗證行為與實際 token 的 aud 組成
tags:
  - keycloak
  - oauth2.0
  - oidc
---

## Keycloak 發生錯誤

想要取得用戶透過 OIDC 登入時的 ID Token 跟 Access Token 的資料結構，使用工具 Keycloak 26.7.1 > Clients > Client scopes -> Evaluate 進行模擬。帶入下面參數進行模擬，會發生錯誤 Danger alert:Requested audience not available: grafana_dlqlr63acgdf

- Realm：master
- Scope parameter: openid
- Users: justin.lee
- Target audience: grafana_dlqlr63acgdf
- grafana_dlqlr63acgdf client：未配置任何 Audience Mapper。

## Keycloak log 分析

- Evaluate 傳入 audience=grafana_dlqlr63acgdf 時，Keycloak 在 validateAudience 階段拋出 NotFoundException，token 產生流程中止（未產生 token）。
- 透過 Grafana 的 log 紀錄 resource_access = { grafana_dlqlr63acgdf, account }，而 aud = [ account ]，差集恰為發起請求的 client 自身，可以判斷 Keycloak 的 audience 解析僅涵蓋「使用者持有角色的其他 client」，不含發起請求的 client 自身（該身分由 azp 承載）。因此以自身 client id 作為 target audience 時查無此 audience。
- 待驗證：ClientScopeEvaluateResource.java:416 的實作，或 Keycloak 官方文件對 Evaluate 的 audience 參數說明。

```
2026-08-11 07:46:20,382 DEBUG [io.quarkus.vertx.http.runtime.ForwardedParser] (vert.x-eventloop-thread-1) Recalculated absoluteURI to https://keycloak.example.com/admin/realms/master/clients/53b42e27-3030-4e16-8a15-e3f7650480f0/evaluate-scopes/generate-example-access-token?userId=eedecfd8-dac7-42a9-863a-28c270b57918&scope=openid&audience=grafana_dlqlr63acgdf

2026-08-11 07:46:20,399 DEBUG [org.keycloak.services.resources.admin.ClientScopeEvaluateResource] (executor-thread-2) generateExampleAccessToken invoked. User: justin.lee, Scope param: openid, Target Audience: grafana_dlqlr63acgdf

2026-08-11 07:46:20,428 DEBUG [org.keycloak.services.error.KeycloakErrorHandler] (executor-thread-2) Error response Not Found: jakarta.ws.rs.NotFoundException: Requested audience not available: grafana_dlqlr63acgdf
        at org.keycloak.services.resources.admin.ClientScopeEvaluateResource.validateAudience(ClientScopeEvaluateResource.java:416)
        at org.keycloak.services.resources.admin.ClientScopeEvaluateResource.lambda$generateExampleAccessToken$5(ClientScopeEvaluateResource.java:286)
        at org.keycloak.services.resources.admin.ClientScopeEvaluateResource.sessionAware(ClientScopeEvaluateResource.java:384)
        at org.keycloak.services.resources.admin.ClientScopeEvaluateResource.generateExampleAccessToken(ClientScopeEvaluateResource.java:281)
        at org.keycloak.services.resources.admin.ClientScopeEvaluateResource$quarkusrestinvoker$generateExampleAccessToken_fc7d9244a5e406c75f367614e7dd45fe6668ca68.invoke(Unknown Source)
        at org.jboss.resteasy.reactive.server.handlers.InvocationHandler.handle(InvocationHandler.java:29)
        at org.keycloak.quarkus.runtime.integration.resteasy.TransactionalSessionHandler.handle(TransactionalSessionHandler.java:85)
        at io.quarkus.resteasy.reactive.server.runtime.QuarkusResteasyReactiveRequestContext.invokeHandler(QuarkusResteasyReactiveRequestContext.java:190)
        at org.jboss.resteasy.reactive.common.core.AbstractResteasyReactiveContext.run(AbstractResteasyReactiveContext.java:147)
        at io.quarkus.vertx.core.runtime.VertxCoreRecorder$15.runWith(VertxCoreRecorder.java:677)
        at org.jboss.threads.EnhancedQueueExecutor$Task.doRunWith(EnhancedQueueExecutor.java:2651)
        at org.jboss.threads.EnhancedQueueExecutor$Task.run(EnhancedQueueExecutor.java:2630)
        at org.jboss.threads.EnhancedQueueExecutor.runThreadBody(EnhancedQueueExecutor.java:1622)
        at org.jboss.threads.EnhancedQueueExecutor$ThreadBody.run(EnhancedQueueExecutor.java:1589)
        at org.jboss.threads.DelegatingRunnable.run(DelegatingRunnable.java:11)
        at org.jboss.threads.ThreadLocalResettingRunnable.run(ThreadLocalResettingRunnable.java:11)
        at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
        at java.base/java.lang.Thread.run(Thread.java:1583)
```

## Grafana log 分析

- Grafana 作為 client，登入時從 ID Token 與 Access Token 抽取 user info（log 中 source=id_token、source=access_token 各一次），但不校驗 access token 的 aud —— 該校驗是 resource server 的職責。因此 aud 不含 grafana_dlqlr63acgdf 不影響登入

```
logger=oauth.generic_oauth t=2026-08-11T06:04:18.953158393Z level=debug msg="Extracting user info from OAuth ID token"
logger=oauth.generic_oauth t=2026-08-11T06:04:18.95359253Z level=debug msg="Parsed user info from JSON" raw_json="{\"exp\":1786428558,\"iat\":1786428258,\"auth_time\":1786428255,\"jti\":\"11111111-1111-1111-1111-111111111111\",\"iss\":\"https://keycloak.example.com/realms/master\",\"aud\":\"grafana_dlqlr63acgdf\",\"sub\":\"22222222-2222-2222-2222-222222222222\",\"typ\":\"ID\",\"azp\":\"grafana_dlqlr63acgdf\",\"sid\":\"M8qwAEmOniUT8saescie1qTN\",\"at_hash\":\"xTisnruSVfR4wgTlmHyLMw\",\"acr\":\"1\",\"resource_access\":{\"grafana_dlqlr63acgdf\":{\"roles\":[\"grafana-admin\"]}},\"email_verified\":true,\"name\":\"lee justin\",\"preferred_username\":\"justin.lee\",\"given_name\":\"lee\",\"family_name\":\"justin\",\"email\":\"email@gmail.com\"}" data="Name: lee justin, Displayname: , Login: , Username: , Email: email@gmail.com, Upn: , Attributes: map[]" source=id_token

logger=oauth.generic_oauth t=2026-08-11T06:04:19.207993071Z level=debug msg="Extracting user info from OAuth access token"
logger=oauth.generic_oauth t=2026-08-11T06:04:19.208450198Z level=debug msg="Parsed user info from JSON" raw_json="{\"exp\":1786428558,\"iat\":1786428258,\"auth_time\":1786428255,\"jti\":\"ofrtac:35af2004-2afb-c99c-c5d7-8219a72b7be8\",\"iss\":\"https://keycloak.example.com/realms/master\",\"aud\":[\"account\"],\"sub\":\"22222222-2222-2222-2222-222222222222\",\"typ\":\"Bearer\",\"azp\":\"grafana_dlqlr63acgdf\",\"sid\":\"M8qwAEmOniUT8saescie1qTN\",\"acr\":\"1\",\"allowed-origins\":[\"https://grafana.example.com\"],\"realm_access\":{\"roles\":[\"default-roles-master\",\"offline_access\",\"uma_authorization\"]},\"resource_access\":{\"grafana_dlqlr63acgdf\":{\"roles\":[\"grafana-admin\"]},\"account\":{\"roles\":[\"manage-account\",\"manage-account-links\",\"view-profile\"]}},\"scope\":\"openid offline_access email profile\",\"email_verified\":true,\"name\":\"lee justin\",\"preferred_username\":\"justin.lee\",\"given_name\":\"lee\",\"family_name\":\"justin\",\"email\":\"email@gmail.com\"}" data="Name: lee justin, Displayname: , Login: , Username: , Email: email@gmail.com, Upn: , Attributes: map[]" source=access_token
```

## 結論

- Evaluate 以自身 client id 作為 target audience 時，Keycloak 在 validateAudience 就中止並回 404，token 未被產生。錯誤描述的是「查無此 audience 設定」，不是「產生的 token 受眾不符」。
- Grafana 是 client 而非 resource server，從未校驗 access token 的 aud。
- 本環境目前沒有任何 resource server 在消費 access token，aud 的內容因此尚未產生實際效果。
- 註：本文 log 已去識別化，jti、sub、sid、domain、email 為替換值；其餘未列出者均為原值。
