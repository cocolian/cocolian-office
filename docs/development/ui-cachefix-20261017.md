状态：2026-10-17 已全部撤回；下文为历史记录，当前状态见 ui-full-rollback-20261017.md。

# 图标标题仍显示的缓存修复

用户提供的截图确认旧页面仍显示 Save、Print、下载、修复、属性、安全标签、签名等按钮标题。服务器镜像已包含隐藏标题的 CSS，但上次 UI 修改沿用了 `19b4efae7f` 的资源路径和 ETag；FileServer 设置 `max-age=11059200`（128 天），旧浏览器缓存可能继续命中。

本次先添加本地构建脚本 `scripts/set-ui-build-revision.py`，以基础提交与本地 browser 补丁派生独立 UI 版本，再写入构建快照的 dist_git_hash，重新 configure、编译及安装 coolwsd/browser，不混换文档引擎。当前 UI 版本为 `a6f66c88cb`，基础提交仍为 `19b4efae7fb8e9eda4a6d88baa959c838d3eb8c3`。

同一浏览器上下文、独立本地测试文档的升级回归结果：

- 旧版 File 标签可见标题：Save、Print、下载、修复、属性、安全标签、签名。
- 旧资源 `/browser/19b4efae7f/bundle.css`、bundle.js；新版 `/browser/a6f66c88cb/bundle.css`、bundle.js。
- 未清空浏览器缓存，切换新版后 10 个标签页中已渲染的图标按钮标题隐藏，原有名称保留用于 tooltip 与 aria-label。
- 实际悬浮提示“粘贴 (Ctrl+V)”与“替换”通过；字体、字号、样式选择值与标签页名保留。
- 独立 Alice/Bob 编辑和 WOPI 保存通过。

镜像 `registry.example.invalid/cocolian/collabora-source:tabbed-icons-cachefix-20261016`，不可变摘要 `sha256:676442121b7dbb054e14401b66efa23cb43b37b1f22f9a0b6df06cb06026db71`。已推送仓库，由 k3s 实际拉取后更新 office-lab/collabora，rollout 成功。门户和转换服务镜像未改变。

线上内部接口报告 productVersionHash=a6f66c88cb，DOCX 转 PDF HTTP 200、24725 字节，中文文本提取通过。其他 11 个 Pod 的 UID/imageID/ready/restartCount 均未变化。没有读取受浏览器权限限制的用户 Chrome 页面；上述 UI 验收在开发机回环测试环境完成。

本地 `work/ui-cachefix-20261016/` 保存发布前 Deployment、Pod 和文档备份、回滚补丁与验收证据。开发机对应资料位于 `build/source-19b4efae7fb8/ui-cachefix-20261016/`，浏览器缓存回归结果与截图位于 `artifacts/ui-cachefix-20261016/`。

后续修改 browser 后，必须先运行 `python3 scripts/set-ui-build-revision.py src/online.mirror build/source-19b4efae7fb8/source`，再重新 configure、编译 server/browser、打包发布；不能只换 CSS 后继续使用旧版本号。只生成版本文件而不重新编译不生效。当前已打开的旧页面需关闭后重新进入编辑页面，新页面会加载新版本资源。
