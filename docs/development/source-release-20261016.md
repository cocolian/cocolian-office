# 2026-10-16 源码镜像仓库发布

> 地址和目录均为通用示例，实际部署值应由自己的私有配置提供。


已将 build-host 的源码构建产物通过现有 registry 发布到 office-lab。工作目录 `<workspace>/cocolian-office`。本次复用已成功完成的全源码编译与 OCI 打包，没有重复全量编译。

## 版本与镜像

源码来自 `https://github.com/cocolian/online.mirror`，提交 `19b4efae7fb8e9eda4a6d88baa959c838d3eb8c3`。包含配套 engine、coolwsd、browser，版本 26.04.6.0。独立 `office-core` 主干未混入此次构建。

| Deployment | Registry 镜像 | SHA256 |
|---|---|---|
| collabora | registry.example.invalid/cocolian/collabora-source:src-19b4efae7fb8 | e52c1ff4995d901f4ff62620f881aa6f4ecb64a5e108fac7f6fc5429497ba894 |
| libreoffice | registry.example.invalid/cocolian/libreoffice-source:src-19b4efae7fb8 | dc1b94c5668ee37cad71f3307a17eb40dec70d458c1ad8c53166eec0ad38bfd7 |

Deployment 使用仓库全名及不可变摘要，不使用可变标签定位。pullPolicy 从 Never 改为 IfNotPresent，允许节点按已有 registry 配置拉取。发布时已实际执行 k3s crictl pull，两镜像成功从仓库拉取，再切换 Deployment。不是离线导入。

## 流程与入口

开发机已有入口：`scripts/compile-source.sh`、`scripts/export-source-images.sh`；构建日志末尾 ALL_SOURCE_BUILDS_COMPLETE、容器退出码 0。重复构建前按原 source-build.md 说明检查缓存和产物，不删除工作树。

新增 `scripts/push-source-images.sh`：在开发机执行 `bash scripts/push-source-images.sh artifacts /path/to/private-auth.json`，默认使用 127.0.0.1:15000 的临时 SSH 隧道。脚本保留镜像摘要，并校验仓库读取摘要与本地 receipt 一致。不同提交通过 SOURCE_TAG=src-<12位提交> 指定。

本次仓库 HTTPS 证书此前校验失败，未关闭公网 TLS 验证或修改 registry。由 cocoserver 向开发机建立反向 SSH 转发：

```bash
ssh -i ~/.ssh/paymentrpc_rsa -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes \
  -N -R 127.0.0.1:15000:CLUSTER_SERVICE_ADDRESS:80 codex@PRIVATE_NETWORK_ADDRESS
```

仅 loopback 上使用 HTTP，跨机器传输经 SSH 加密。临时认证 JSON 使用已有 registry 账户，权限 0600，不提交 Git；发布后删除并关闭隧道。未更改生产 Namespace 配置、宿主机 DNS、路由或代理。

发布补丁使用 JSON Patch test 验证原 template 后再替换，以防并发覆盖；新镜像 UID/GID=1001，保持非 root、无提权、丢弃 capabilities。Collabora 显式配置 WOPI 白名单；转换服务移除旧 gotenberg 启动参数。

## 验证证据

公网 `https://office.example.invalid`：登录成功；Alice/Bob 独立浏览器均启动编辑器，输入两条独立标记，最终下载 DOCX 同时包含标记；WOPI 保存成功。保留了原文副本及验证后 DOCX。

实际转换：服务内与公网 POST /convert/forms/libreoffice/convert 均得到有效 PDF；公网 HTTP 200，24725 字节，PDF 文本提取包含“国产在线文档中台：中文渲染与保存验证。”及“源码编译验证”。未进行复杂版式视觉验收。

两个新 Deployment 各 1/1，就绪、无重启。WOPI 原 Pod 不变，其他 Namespace 9 个 Pod 的 UID、imageID、ready、restartCount 对比无变化。

## 已知限制

- 源码构建没有引擎翻译仓库；虽然浏览器配置仍请求 zh-CN，截图中菜单和侧栏出现较多英文。中文文档渲染及 PDF 文本验证通过，不代表完整中文界面已通过。
- libreoffice-source 是 CLI 转换适配服务，当前只兼容单文件 DOCX（20 MiB）转 PDF；高级 Gotenberg 参数及其他格式不支持，不能按完整 Gotenberg API 宣称兼容。
- 源码版与旧 CODE 25.04 有较大版本跨度。完整上游测试、复杂版式视觉验收未执行。

## 回滚与备份

本地 `work/release-20261016/` 保存原 Deployment、全集群 Pod 基线、文档卷 tar、并发保护的 rollback JSON、新旧状态及验证截图。整个目录已排除 Git。虚拟机同目录 `build/source-19b4efae7fb8/release-20261016` 保存部署补丁、回滚补丁和状态；`artifacts/release-20261016` 保存在线验证证据。

在开发机执行相应 rollback JSON，恢复旧镜像、参数和 pullPolicy，再等待 rollout；回滚补丁包含当前 template 前置校验，如有后续发布应先检查差异。旧镜像和 PVC 保留，勿删除 PVC。文档备份仅在核对后人工恢复，避免覆盖新增修改。
