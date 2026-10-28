# Cocolian Office 国产化云文档中台

Cocolian Office 的目标是构建国产化的 LibreOffice，建设可自主构建、可私有部署的云文档中台，让中文文档在在线编辑、预览和 PDF 转换时，获得与 Microsoft Office Word 尽可能一致的渲染效果。

项目基于 LibreOffice 和 Collabora Online 持续开发，重点改进中文字体、行距、换行、分页、表格和中英文混排。我们追求最佳的中文文档与 Word 渲染一致性，并以真实对照和回归测试逐项推进这一目标。

**本项目开源，可按各组件许可证免费使用、部署和接入。欢迎参与开发，欢迎将项目接入你的产品，也欢迎捐款支持项目持续维护。**

## 项目能力

- 在线文档编辑与协同，通过 WOPI 连接文档存储、鉴权及保存回调。
- DOCX 预览与 PDF 转换，面向业务系统提供文档处理能力。
- 中文排版兼容性改进，覆盖中文字体匹配、GB2312 和 GBK 字体、文档网格、段落行距、表格跨页及混排规则。
- 从源码构建渲染引擎与在线服务，使用 Docker 镜像部署，并通过自动检查验证发布。

当前以 Mac 版 Microsoft Word 导出的 PDF 作为主要对照基准，对修复前后的字体、文字位置、换行和分页进行比较。复杂文档仍可能存在布局差异，兼容性工作会持续推进。

## 项目组成

| 仓库 | 职责 |
| --- | --- |
| [cocolian-office](https://github.com/cocolian/cocolian-office) | 开发工作区、源码版本组织、构建部署配置和项目文档 |
| [online.mirror](https://github.com/cocolian/online.mirror) | 基于 Collabora 的在线编辑服务及配套渲染引擎，承载主要排版修复 |
| [cocolian](https://github.com/cocolian/cocolian) | 文档门户、WOPI Host 及业务接入 |
| [office-core](https://github.com/cocolian/office-core) | LibreOffice core 源码工作区 |
| [collabora-online-sdk-examples](https://github.com/cocolian/collabora-online-sdk-examples) | 在线文档集成示例 |

本仓库通过 Git submodule 记录相关源码版本；主要渲染修复位于 `src/online.mirror/engine`。具体源码来源见 [repos.json](repos.json)。

## 开始开发

```bash
git clone https://github.com/cocolian/cocolian-office.git
cd cocolian-office
./scripts/setup-dev.sh
```

`setup-dev.sh` 初始化锁定版本的源码仓库。完整源码检出和首次构建可能需要较长时间；需要完整历史时，在对应浅克隆仓库执行 `git fetch --unshallow origin`。

引擎源码构建使用 Linux 环境；Mac 可用于代码开发和 Word 渲染对照。构建说明见 [源码构建文档](docs/development/source-build.md)，容器配方见 [deploy/source-build](deploy/source-build/README.md)。这些文档包含历史构建记录，具体版本以当前代码和部署配置为准。

第三方字体文件不随本仓库分发。部署时请提供有权使用的字体，并保持对照环境与服务端的字体版本一致。

## 接入项目

欢迎文档管理系统、知识库、业务平台和其他应用接入 Cocolian Office。可以通过 WOPI 对接文档打开、编辑与保存，也可以通过转换接口集成 DOCX 转 PDF。

接入实现与接口说明见 [文档门户仓库](https://github.com/cocolian/cocolian)。欢迎通过项目仓库联系维护者，交流接入需求、部署方式和兼容性问题。

## 参与贡献

欢迎贡献排版修复、测试、文档和系统集成。反馈渲染差异时，请说明字体、Word 版本、页面设置和复现步骤，优先提供可公开的最小合成案例。

真实业务文档、私有字体、生成的 PDF、构建产物和凭据应保存在仓库外。提交前请检查文件名及内容，确保具备公开权限。

## 捐款支持

欢迎为本项目捐款，支持中文排版兼容性开发、回归测试和构建资源。也欢迎提供算力、测试环境、代码贡献或集成反馈。

欢迎捐款支持，可通过 [GitHub Issue](https://github.com/cocolian/online.mirror/issues) 联系项目维护者。支持项目不影响按许可证免费使用开源代码。

## 开源许可与上游

感谢 LibreOffice、Collabora Online 及其社区。本项目的相关源码保留上游许可证和版权声明；使用、修改和分发时，请遵守各组件目录中的许可文件。渲染源码仓库的许可证入口见 [COPYING](https://github.com/cocolian/online.mirror/blob/main/COPYING)。

项目介绍与媒体文案见 [项目介绍文章](https://github.com/cocolian/online.mirror/blob/main/cocolian/office-lab/docs/community/introduction-zh.md) 和 [社交媒体文案](https://github.com/cocolian/online.mirror/blob/main/cocolian/office-lab/docs/community/social-posts.md)。

## English

Cocolian Office is an open source cloud document platform built on LibreOffice and Collabora Online. We focus on Chinese document rendering, aiming for the closest possible fidelity to Microsoft Word across online editing, preview and PDF conversion. The project can be used and integrated free of charge under the applicable component licenses. Contributions, integrations and donations are welcome.
