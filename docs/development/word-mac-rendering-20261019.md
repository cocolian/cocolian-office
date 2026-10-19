# Word for Mac 排版兼容配置

## 修复内容

基于现有 26.04.6.0 源码构建，修正 Word 表格网格行距重复乘以比例、网格表格末尾额外行距、字符单位缩进使用错误默认字号、无换行自适应文本框未同步可变宽度的问题。新增两个小型回归文档，只含合成文字和通用页码文本框，无业务正文。

字体配置单独部署为 `collabora-wordmac`。该配置按照参考 Mac Word 的实际字体替代结果，将缺失的仿宋 GB2312、小标宋映射到 Microsoft YaHei，同时提供参考文档使用的微软雅黑、宋体、黑体、等线、Calibri。字体从现有本机 Office 安装目录提供，字体二进制和业务文档不进入 Git。普通渲染服务继续保留原有字体规则。

门户环境变量 `WORD_MAC_DOCUMENT_IDS` 是以逗号分隔的文档 ID 白名单；匹配时使用 `http://collabora-wordmac:9980/word-mac/hosting/discovery`，其余沿用原服务。网关将 `/word-mac/` 代理至兼容服务。新服务使用 `--o:net.service_root=/word-mac`，沿用原 WOPI 白名单、非 root 运行和网络隔离。

## 构建与验收

- 使用 Linux 开发 VM 中已有源码构建缓存；代码先在 Mac 本机修改，再传输增量源码编译。
- 先顺序构建相关库或执行 `CppunitTest_sw_layoutwriter5`，不要并发启动多个共享同一 workdir 的 make。
- 运行 `testWordImportTypography testWordTableGridProportional testTdf144450 testTdf167583`，验证缩进、文本框宽度切换、表格网格及正文行距。
- 运行时必须包含同一构建的 `libswlo.so`、`libmergedlo.so`；如修改导入器，还需包含 `libsw_writerfilterlo.so`。只替换 Writer 库不能包含导入器改动。
- 用 `deploy/source-build/WordMac.Dockerfile` 打包，传入匹配的不可变基础镜像。构建上下文 `program/`、`fonts/` 来自本地私有产物；`word-mac-fontconfig.xml` 来自源码配置。
- 推送到现有私有 registry，以实际校验过的 SHA256 更新 Deployment。保留旧 Deployment、ConfigMap、文档卷备份及 JSON Patch 回滚文件。

参考样本从原先 24 页恢复为 22 页，字体、表格行距、首行缩进和页码位置得到修复。仍存在部分正文换行、字距和跨页文字位置差异，不能据此宣称与 Word 逐像素一致。中文标点压缩设置的通用导入实现未纳入本次变更，因为实际对比会进一步偏离 Mac Word 参考。
