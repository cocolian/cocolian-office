最新状态（2026-10-16）：已发布至 office-lab。下文未发布/权限不足内容为历史构建阶段记录；本次通过 SSH 隧道推送 registry，不使用受限离线导入程序。完整结果、中文界面和 API 限制见 source-release-20261016.md。

> 地址和目录均为通用示例，实际部署值应由自己的私有配置提供。


# 本地全源码构建与 K3s 发布记录

## 范围和版本

本次编译 cocolian/online.mirror 提交 19b4efae7fb8 下的 engine、coolwsd 和 browser。engine 是配套的 LibreOffice/Collabora Office 渲染引擎；不把独立 LibreOffice 主干与不同版本的 Collabora 混配。源码版本为 26.04.6.0，线上基线为 CODE 25.04.9.2。

原 Fork 工作树保持独立，构建使用 build/source-19b4efae7fb8/source 快照。完整提交在该目录 source-lock.json 中。构建容器使用 Debian 13、GCC 14，基础镜像按摘要固定，资源限制为 3 CPU / 12 GiB。71 个外部依赖按生成的 fetch-list.json 下载并验证 SHA-256。

## 操作入口

- deploy/source-build/Builder.Dockerfile：构建工具环境；Debian 镜像源保留官方签名验证。
- deploy/source-build/compile.sh：引擎、服务端、前端的编译及 stage 安装流程。
- scripts/compile-source.sh：首次启动本次快照的编译容器，已有同名容器时停止，避免覆盖。
- scripts/prefetch-source.py：并发预取本次配置的依赖；缓存哈希不匹配时不会当作成功。
- scripts/export-source-images.sh：stage 完成后导出两个单平台 OCI 镜像。
- scripts/normalize-source-oci.py：校验 OCI 路径、摘要、架构及非 root UID，写入导入工具要求的镜像名称。

观察编译：

```bash
docker logs --tail 40 cocolian-source-19b4efae7fb8
docker inspect --format '{{json .State}}' cocolian-source-19b4efae7fb8
```

容器失败后，修复对应问题再执行 `docker start -a cocolian-source-19b4efae7fb8`，会复用已有依赖和编译缓存。不要删除 workdir 作为常规排错步骤。成功标志为日志中的 ALL_SOURCE_BUILDS_COMPLETE，随后确认容器退出码为 0，并检查 stage/usr/bin/coolwsd 和 stage/opt/collaboraoffice/program/soffice.bin。

构建关闭了 Java、Python 脚本、调试符号和附带字体/字典包；运行时提供系统字体。当前源码快照缺少独立的引擎翻译仓库，因此请求的 zh-CN 引擎界面语言会回退到 en-US。中文内容渲染、排序/转换数据与浏览器界面翻译是独立能力，须分别验收。

## 两个运行时镜像

- docker.io/cocolian/collabora-source:src-19b4efae7fb8：源码 coolwsd、浏览器客户端和配套引擎。
- docker.io/cocolian/libreoffice-source:src-19b4efae7fb8：使用同一源码引擎 CLI 的受限转换适配服务；保留当前门户用到的 POST /forms/libreoffice/convert 与 GET /health。只接受单个 DOCX files 字段，未实现的高级 Gotenberg 参数返回 400。基底仍复用固定的 Gotenberg 运行环境，但不启动其 UNO 客户端。

OCI 导出包和对应摘要 JSON 存放在 artifacts。Docker 构建上下文只包含 stage 和 runtime-tools，避免把源码、缓存或部署备份写入镜像。两个运行时均使用 1001:1001。导出脚本不会自动发布或覆盖已有导出包。

## 验证与发布前提

已有基线：tests/fixtures/source-build-smoke.docx 在线上转换服务得到 HTTP 200、application/pdf 和有效 PDF 文件头，大小 23629 字节。该结果只证明基线转换成功，不代表新源码引擎通过测试，也未验证版式或文本提取。

本地编辑验收副本位于 tests/integration/wopi-source-host.py，基于原门户实现，只绑定 127.0.0.1:18080，文档目录由 SOURCE_TEST_DATA 指定，测试密钥通过 LAB_KEY 临时提供。新版 Collabora 测试端口为 19980。不得用真实线上数据目录或在命令输出中打印密钥。

已通过：源码引擎版本与 CLI 转换、Collabora 运行镜像转换及中文 PDF 文本、Alice/Bob 两个独立浏览器登录并打开同一文档、双方输入标记并在最终 WOPI DOCX 中同时保留、转换适配服务 HTTP 200 与中文 PDF 文本、未实现参数返回 400、OCI 路径/摘要/架构/UID 校验。未进行复杂版式视觉验收、完整上游测试套件或线上源码版验收。

新引擎 UNO 类型使用 cpo 命名，与基底 Gotenberg unoconverter 的 com.sun.star 类型不兼容；此外移除了 nocrashreport 开关和旧首次启动退出行为。最终服务采用 CLI，未修改引擎 UNO 源码，也不声称兼容完整 Gotenberg 功能。编译阶段的 make build 不等于已运行完整单元测试。

现有 K3s 部署位于 office-lab，镜像拉取策略为 Never。应先将 OCI 包导入宿主机 containerd，再按不可变摘要更新对应 Deployment；保留原镜像、配置和 PVC，验证失败时回滚。正式发布前重新保存部署与 Pod 基线，并检查配置是否出现并发变更。

当前发布通道存在两个前置条件：registry.example.invalid 的证书校验报告过期；office-image-host SSH 密钥只能调用受限导入程序，当前仅接受 office-portal 镜像。deploy/source-build/import-office-image.proposed.py 是新增两个源码镜像仓库的受限扩展提案，未安装；仍需宿主机管理员核对并安装，或提供已可用的安全镜像发布通道。不得使用 office-portal 名称绕过仓库限制。

部署前快照位于 build/source-19b4efae7fb8/baseline。当前记录阶段为全源码构建成功、本地冒烟验收通过、两个 OCI 包已生成；宿主机导入权限尚未补齐，未发布源码镜像。测试结果位于同目录 source-*-smoke.json；浏览器截图和完整编译日志位于 logs。
