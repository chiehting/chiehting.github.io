---
date: 2021-06-24T14:39:00+0800
updated: 2023-07-31T17:07:25+08:00
title: Linux kernel 的網路參數 rp_filter
category: operating-system
tags:
  - operating-system
  - linux
  - internet
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
post: true
---

這篇來記錄有關 Linux kernel 的 network 參數。

<!--more-->

### rp_filter

為逆向路徑過濾 (Reverse Path Filtering)，其作用為為過濾反向不通的封包，將其丟棄。
而原理為由 NIC1 (network interface card) 進來的封包，reverse path filtering 模塊會將其封包的源地址（source ip）與目標地址（destination ip）做對調，然後再路由表中查找，如果出去的介面是 NIC1 則通過；反之不是 NIC1 則丟棄該封包。

可以從 [ip-sysctl](https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt) 文件中找到參數的用法。其中該參數為整數型，其值包括了 0：不做來源驗證；1：嚴謹認證模式；2：寬鬆認證模式。

    rp_filter - INTEGER
        0 - No source validation.
        1 - Strict mode as defined in RFC3704 Strict Reverse Path
            Each incoming packet is tested against the FIB and if the interface
            is not the best reverse path the packet check will fail.
            By default failed packets are discarded.
        2 - Loose mode as defined in RFC3704 Loose Reverse Path
            Each incoming packet's source address is also tested against the FIB
            and if the source address is not reachable via any interface
            the packet check will fail.

    Current recommended practice in RFC3704 is to enable strict mode
        to prevent IP spoofing from DDos attacks. If using asymmetric routing
        or other complicated routing, then loose mode is recommended.

    The max value from conf/{all,interface}/rp_filter is used
        when doing source validation on the {interface}.

    Default value is 0. Note that some distributions enable it
        in startup scripts.

#### Source code

可以上網找到原始碼 [fib_frontend.c](https://elixir.bootlin.com/linux/latest/source/net/ipv4/fib_frontend.c#L419)，這邊來看一下實作方法。

```c
/* Ignore rp_filter for packets protected by IPsec. */
int fib_validate_source(struct sk_buff *skb, __be32 src, __be32 dst,
            u8 tos, int oif, struct net_device *dev,
            struct in_device *idev, u32 *itag)
{
    /* 是否啟用反向封包過濾功能，這邊注意如果封包受 IPSec 保護則忽略反向封包過濾功能 */
    int r = secpath_exists(skb) ? 0 : IN_DEV_RPFILTER(idev);
    struct net *net = dev_net(dev);

    if (!r && !fib_num_tclassid_users(net) &&
        (dev->ifindex != oif || !IN_DEV_TX_REDIRECTS(idev))) {
        /* 本地源的封包不執行反向封包過濾功能 */
        if (IN_DEV_ACCEPT_LOCAL(idev))
            goto ok;
        /* with custom local routes in place, checking local addresses
        * only will be too optimistic, with custom rules, checking
        * local addresses only can be too strict, e.g. due to vrf
        */
        if (net->ipv4.fib_has_custom_local_routes ||
            fib4_has_custom_rules(net))
            goto full_check;
        if (inet_lookup_ifaddr_rcu(net, src))
            return -EINVAL;

ok:
        *itag = 0;
        return 0;
    }

full_check:
    return __fib_validate_source(skb, src, dst, tos, oif, dev, r, idev, itag);
}
```


```c
static int __fib_validate_source(struct sk_buff *skb, __be32 src, __be32 dst,
                u8 tos, int oif, struct net_device *dev,
                int rpf, struct in_device *idev, u32 *itag)
{
    struct net *net = dev_net(dev);
    struct flow_keys flkeys;
    int ret, no_addr;
    struct fib_result res;
    struct flowi4 fl4;
    bool dev_match;

    fl4.flowi4_oif = 0;
    fl4.flowi4_iif = l3mdev_master_ifindex_rcu(dev);
    if (!fl4.flowi4_iif)
        fl4.flowi4_iif = oif ? : LOOPBACK_IFINDEX;
    /* 可以看到這邊做反轉了 */
    fl4.daddr = src;
    fl4.saddr = dst;
    fl4.flowi4_tos = tos;
    fl4.flowi4_scope = RT_SCOPE_UNIVERSE;
    fl4.flowi4_tun_key.tun_id = 0;
    fl4.flowi4_flags = 0;
    fl4.flowi4_uid = sock_net_uid(net, NULL);
    fl4.flowi4_multipath_hash = 0;

    no_addr = idev->ifa_list == NULL;

    fl4.flowi4_mark = IN_DEV_SRC_VMARK(idev) ? skb->mark : 0;
    if (!fib4_rules_early_flow_dissect(net, skb, &fl4, &flkeys)) {
        fl4.flowi4_proto = 0;
        fl4.fl4_sport = 0;
        fl4.fl4_dport = 0;
    }

    if (fib_lookup(net, &fl4, &res, 0))
        goto last_resort;
    if (res.type != RTN_UNICAST &&
        (res.type != RTN_LOCAL || !IN_DEV_ACCEPT_LOCAL(idev)))
        goto e_inval;
    fib_combine_itag(itag, &res);

    dev_match = fib_info_nh_uses_dev(res.fi, dev);
    /* This is not common, loopback packets retain skb_dst so normally they
    * would not even hit this slow path.
    */
    dev_match = dev_match || (res.type == RTN_LOCAL &&
                dev == net->loopback_dev);
    if (dev_match) {
        ret = FIB_RES_NHC(res)->nhc_scope >= RT_SCOPE_HOST;
        return ret;
    }
    if (no_addr)
        goto last_resort;
    if (rpf == 1)
        goto e_rpf;
    fl4.flowi4_oif = dev->ifindex;

    ret = 0;
    if (fib_lookup(net, &fl4, &res, FIB_LOOKUP_IGNORE_LINKSTATE) == 0) {
        if (res.type == RTN_UNICAST)
            ret = FIB_RES_NHC(res)->nhc_scope >= RT_SCOPE_HOST;
    }
    return ret;

last_resort:
    if (rpf)
        goto e_rpf;
    *itag = 0;
    return 0;

e_inval:
    return -EINVAL;
e_rpf:
    return -EXDEV;
}
```

參數：

* struct sk_buff - socket buffer
* __be32 src - source
* __be32 dst - destination
* [struct net_device](https://elixir.bootlin.com/linux/latest/source/include/linux/netdevice.h#L1853) - 網路結構體
* [struct in_device](https://elixir.bootlin.com/linux/latest/source/include/linux/inetdevice.h#L25) - 網路結構體
* saddr - start address
* daddr - destination address

科普：

* __bet32 - le 與 be 分別表示 little endian 和 big endian
* u8、u32 - 表示無符號 char 字符類型

#### 作用

當前RFC3704文檔建議使用嚴謹認證模式。如果網路是非對稱網路或複雜的網路 rp_filter 建議配置為 2，做寬鬆認證。
而 rp_filter 配置作用通常為下列：

1. 減少 DDoS 攻擊，注意是減少不是防止
1. 防止 IP Spoofing

