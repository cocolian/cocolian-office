状态：2026-10-17 已全部撤回；下文为历史记录，当前状态见 ui-full-rollback-20261017.md。

# 默认标签栏及图标悬浮提示（2026-10-16）

已按“本地代码修改 → 编译打包 → 推送 registry.example.invalid → k3s 拉取 → office-lab 更新 → 验收”完成。

## 配置和源码边界

`apps/office-portal/editor.json` 的 `ui_mode` 从 `compact` 改为 `tabbed`，继续请求 zh-CN 和 SavedUIState=false。默认标签栏可直接配置。

当前源码版本没有面向集成方的全局“所有图标隐藏名称”开关；内部 noLabelsForUnoButtons 会被部分大按钮覆盖。因此这部分修改源码：

- `browser/css/notebookbar.css`：只隐藏标签栏中确有图标的按钮 caption，调整其按钮宽度；隐藏分组底部重复标题。标签页名、纯文本控件、字体/字号当前值和样式预览保留。
- `browser/src/control/Control.JSDialogBuilder.js`：原先有名称且无显式 tooltip/快捷键的按钮会主动关闭 tooltip；现在标签栏有图标的按钮仍注册原有悬浮提示事件。保留 aria-label，不删除名称文本或可访问名称。

本地补丁：`patches/collabora/notebookbar-icon-tooltips.patch`，SHA256 `90d73f1da819e2d9ee66cb3c5c63bae1748db532289fa33cae9f53acc1ea0b39`。

开发机源码位于 `<workspace>/cocolian-office/src/online.mirror`，工作分支 `feature/notebookbar-icon-tooltips`，修改保留在工作树，未自动提交或推送 GitHub。同步修改了本次构建快照，前端 make、CSS stylelint、JS eslint 和相关类型检查通过，编译容器退出码 0。没有重编译或更换文档引擎。

## 本次镜像

| 服务 | 仓库标签 | 不可变 SHA256 |
|---|---|---|
| Collabora | registry.example.invalid/cocolian/collabora-source:tabbed-icons-20261016 | 6ca12f11d1ac28d34a0706f17b751647f5e9e58042dc2edbf3304580913f7d4c |
| 门户/WOPI | registry.example.invalid/cocolian/office-portal:tabbed-icons-20261016 | 825553905cc88f90b7be592f2c84e6ddd73e453fd4177bd024923727a15e750e |

镜像通过仅绑定回环地址的临时 SSH 隧道推送仓库，避免大镜像经公网绕行；SSH 对跨机器流量加密。k3s 节点已实际从仓库拉取，Deployment 使用摘要与 IfNotPresent。镜像仓库 HTTPS 证书有效，使用隧道是内网传输方式选择，不是跳过公网证书校验。

## 验证

先在开发机仅绑定 loopback 的候选服务中，用独立测试文档验证；随后在公网服务再次验证，均不注入 CSS、不绕过 CSP：

- 默认标签栏；文件、开始、插入、布局、引用、审阅、格式、表单、查看、帮助共 10 个标签页。
- 已渲染的带图标按钮不显示名称，原带名称按钮有 tooltip，按钮可访问名称保留；实际鼠标悬浮显示“粘贴 (Ctrl+V)”。样式滚动箭头原本不带文字名称，不将其作为 caption 改造对象。
- Alice/Bob 独立浏览器打开编辑器、分别输入标记，下载的 WOPI DOCX 同时包含标记；保留原文备份。
- 公网 DOCX 转 PDF 返回 HTTP 200、有效 PDF，24725 字节。
- 其他 Namespace 的 9 个 Pod UID、imageID、ready、restartCount 不变；LibreOffice 转换 Pod 同样不变。

现有引擎翻译资源不完整的限制未在此次处理；部分英文界面或样式名称仍可能出现。

## 备份与后续操作

本地 `work/tabbed-icons-20261016` 保存原 Deployment、Pod 基线、文档卷 tar、并发保护的发布/回滚补丁、验收结果和截图，已排除 Git。

开发机 `build/source-19b4efae7fb8/tabbed-icons-20261016` 保存回滚资料，`artifacts/tabbed-icons-20261016` 保存公网验收；`baseline/tabbed-icons-browser-smoke.json` 保存候选镜像结果。原镜像与 PVC 保留。

后续仍先修改 Git 工作树中的代码或本地配置，再构建推送镜像，不直接编辑 Pod 内文件。旧编辑页面需要关闭后重新打开；若浏览器缓存仍显示旧布局，执行强制刷新（Mac：Command+Shift+R）。
