# 镜像仓库证书同步记录（2026-10-16）

edge-proxy 当前使用的 Let's Encrypt 证书未过期，不需要重新签发。现有签发/续期脚本为 `/home/cocolian/renew_cert.sh`，需 sudo 执行；使用 certbot dns-aliyun。脚本包含敏感配置，不复制到仓库。

- 源证书：edge-proxy `/etc/letsencrypt/live/example.invalid/fullchain.pem`，配套 privkey.pem。
- 有效期：2026-08-27 08:34:16 UTC 至 2026-11-25 08:34:15 UTC（北京时间 11 月 25 日 16:34:15）。
- SAN：`*.example.invalid`、`example.invalid`。
- 序列号：`05F3D461CC334699230FE314A42AF17D2C5C`。
- 镜像仓库旧证书于 2026-08-23 12:26:21 UTC 过期，导致此前 HTTPS 校验失败。

已通过 SSH 加密流将证书和私钥传输到 cocoserver，校验证书域名、有效期及密钥匹配，再更新 `applications/res-cocolian-cn-tls`。该 Secret 仅被 registry Ingress 引用。旧 Secret 备份在 cocoserver `/root/registry-tls-backups/20261016-215338.json`，目录 0700、文件 0600。私钥没有落地本地工作目录，也未写入本记录。

Ingress 自动加载更新，未重启 registry 或应用 Pod。直接连接 k3s Ingress 的 openssl 校验为 `Verify return code: 0 (ok)`，HTTPS `/v2/` 返回 401（未提供认证的正常结果），curl TLS 校验码为 0；开发虚拟机也验证 HTTPS 证书受信任。仓库实际提供的新证书序列号与 edge-proxy 一致。

可复用 `scripts/sync-registry-certificate.py`，该脚本需在 cocoserver 以 root 运行，stdin 接受可信 SSH 传来的仅包含 fullchain.pem、privkey.pem 的 tar 流。不会输出私钥；更新前自动备份 Secret，并通过 resourceVersion 防止并发覆盖。

未修改宿主机 registries.yaml 的 HTTP 拉取端点。此次只完成证书同步，不新增自动跨主机同步计划；以后 edge-proxy 续期后仍需同步目标 Secret。旧发布文档中的证书过期与 SSH 隧道说明是本次修复之前的历史情况。
