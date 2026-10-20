# main 分支独立触发部署

build-host 约每分钟检查三个项目的 main；任何一个项目有新提交，都会重新构建、推送及部署它拥有的模块。

| 更新的仓库 main | 自动部署模块 |
| --- | --- |
| cocolian | wopi 门户 |
| cocolian-office | collabora、collabora-wordmac、libreoffice |
| online.mirror | collabora、collabora-wordmac、libreoffice |

多个项目同时更新取部署模块并集。未选中的模块保持原镜像及 Pod，不会重启。部署范围为现有 office-lab。引擎使用 online.mirror/main 的实际提交，不等待本仓库更新子模块固定提交号；每次发布记录所有实际源码提交以便追溯。引擎或浏览器源码未变时可复用编译缓存，但选定模块仍重新打包发布。

流程保留候选镜像检查、串行发布、失败回滚和 WOPI 保存/文档转换验证。

[完整流程、日志和运维命令](https://github.com/cocolian/online.mirror/blob/main/cocolian/office-lab/scripts/devops/README.md)
