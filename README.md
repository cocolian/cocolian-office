# 国产开源在线文档中台开发工作区

本仓库保存中台开发资料，并以 Git submodule 锁定三个独立源码仓库。

## 源码

| 目录 | Fork (origin) | 直接上游 (upstream) | 基线分支 |
| --- | --- | --- | --- |
| src/office-core | cocolian/office-core | LibreOffice/core | master |
| src/online.mirror | cocolian/online.mirror | CollaboraOnline/online.mirror | office-ui-20261017 |
| src/collabora-online-sdk-examples | cocolian/collabora-online-sdk-examples | CollaboraOnline/collabora-online-sdk-examples | master |

首次 Clone 使用 --filter=blob:none，保留完整提交历史，文件内容按需下载；首次 checkout 仍可能耗时较长。未执行源码构建或子模块初始化。仓库地址清单见 repos.json。

## 目录职责

- services/wopi：文档存储、鉴权、打开与保存回调服务。
- services/wps-adapter：根据现有业务实际调用设计 WPS 兼容适配层。
- deploy/compose：本地集成环境；deploy/k3s：远程 office-test 命名空间部署配置。
- tests/fixtures：脱敏测试文档；integration：打开、编辑、保存及协同测试；compatibility：中文字体、分页、表格与 DOCX 转 PDF 测试。
- docs/architecture、development、licensing：架构、开发及许可证核查资料。
- build、artifacts：本地构建与测试产物；禁止提交凭据或真实业务文档。

这些目录是开发骨架，尚未实现 WOPI、部署服务或执行功能测试。

## 上游同步

执行 `./scripts/sync-upstream.sh` 仅拉取 upstream，不修改工作树、不推送 Fork。

在工作树干净时，以 office-core 为例：

```bash
cd src/office-core
git switch master
git merge --ff-only upstream/master
# 检查并测试后，按需执行：
git push origin master
# 独立功能开发：
git switch -c feature/your-change
```

online.mirror 使用 main，其余两个仓库使用 master。若 fast-forward 失败，先检查双方提交差异，再决定合并方案；不自动 rebase 或强制推送。每个仓库配置 pull.ff=only、fetch.prune=true 和 remote.pushDefault=origin。upstream 的 push URL 被禁用以防误推。

## 后续验证

先用官方容器建立运行基线，再准备源码编译依赖。远程部署前检查服务器资源、Ingress、TLS 与存储；在线编辑/保存、双客户端协同及格式转换需在真实服务部署后验证。许可证和商用条件应按具体版本另行核查。

## 全源码构建

本次构建与发布说明见 [docs/development/source-build.md](docs/development/source-build.md)。源码编译与打包已完成，2026-10-16 已推送 registry.example.invalid 并发布 office-lab；结果和限制见 docs/development/source-release-20261016.md。

## 本机开发（2026-10-18 迁移）

工作目录：`<workspace>/cocolian-office`。门户源码位于同级 `../cocolian`。

```bash
git clone git@github.com:cocolian/cocolian-office.git
cd cocolian-office
./scripts/setup-dev.sh
```

`repos.json` 和 Git submodule 记录迁移时的精确提交；setup-dev.sh 只初始化这三个源码仓库，不递归下载引擎内部的附加子模块。首次完整检出锁定版本源码，并使用浅克隆减少历史下载；需要完整历史时在对应源码仓库执行 `git fetch --unshallow origin`。源码构建仍需 Linux 环境；Mac 用于编辑、提交和本地可用的验证。构建镜像、缓存、凭据和运行数据不随源码迁移。原服务器工作目录保留。

中文翻译源码另用 `./scripts/setup-translations.sh` 恢复到引擎的 `engine/translations`（上游提交 `17fb3698d5e86169d44076f7a992c572f8f780f1`，仅检出 `source/zh-CN`）。服务器的两份未提交翻译修改已逐字核对，与已提交补丁 `patches/translations/zh-cn-native-commands.patch` 完全一致；恢复后在翻译仓库中显示为修改，这是补丁的预期状态。该官方仓库的推送已禁用。
