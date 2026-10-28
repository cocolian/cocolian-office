# 2026-10-17 撤回标签栏与隐藏标题修改

> 地址和目录均为通用示例，实际部署值应由自己的私有配置提供。


按用户确认，撤回全部默认标签栏、隐藏图标标题和后续缓存版本修改，恢复这些 UI 改动前的界面；不是回退至最初 CODE 25.04 官方镜像。

- Collabora 恢复 `registry.example.invalid/cocolian/collabora-source@sha256:e52c1ff4995d901f4ff62620f881aa6f4ecb64a5e108fac7f6fc5429497ba894`，版本 26.04.6.0，资源版本 19b4efae7f。
- 门户恢复 `docker.io/cocolian/office-portal@sha256:877522cb9df4cfe3d6903f7584a1c37164f3e4ff8dcd0c40e7c662fc9319222e`，ui_mode=compact，保留 zh-CN 与 SavedUIState=false。
- 两个 Deployment 完整 template 与原始备份一致，rollout 均成功，编辑器和转换健康接口均 HTTP 200。原 gateway、转换镜像和其他 Namespace 不变。
- 没有回写、替换或删除任何文档/PVC。

开发机 `src/online.mirror` 中的 notebookbar.css 和 Control.JSDialogBuilder.js 修改通过反向补丁精确撤回，恢复 main，Git 工作树干净。修改前检查了差异 SHA256，以免覆盖并发变更。

本机及开发机 editor.json 恢复 compact。新增 UI 缓存构建脚本和相关验收脚本移至备份，不再作为活动流程；构建快照源码、dist_git_hash 恢复原版，重新生成原 server/browser 构建产物。

此前的发布报告和补丁仅作历史记录保留。现场备份和本次结果在本机 `work/tabbed-icons-20261016`；开发机原回滚补丁和归档源码工具在 `build/source-19b4efae7fb8/tabbed-icons-20261016`。

用户已打开的页面仍需关闭后重新打开，才会加载恢复后的界面。
