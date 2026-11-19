# 访谈切片工作流 Skill

适用于真实访谈、演讲和原声二创：从脚本取舍、高清源、原声剪辑、双语字幕、阶段核心提炼、素材补充到封面、配乐、审片和归拢清理。不是数字人口播工具。

本包按资讯 Skill 的完整提炼和分发过程组织：**详细规则＋可运行独立工程＋真实字体校验＋逐项验收＋安装验证**。本地版本1.0.0；GitHub公开发布与安装核验结果见VALIDATION.md。

## 使用

公开仓库地址：https://github.com/Predirector/interview-slice-workflow

在Codex中发送：

```text
使用 Skill Installer 安装：
https://github.com/Predirector/interview-slice-workflow/tree/main/skills/interview-slice-workflow
```


安装整个 `skills/interview-slice-workflow` 文件夹到你当前Codex支持的用户技能目录（常见 `~/.codex/skills`），不能只复制SKILL.md。安装后调用 `$interview-slice-workflow`；如果当前会话技能清单尚未刷新，重新打开聊天。

可复制的首次请求：

> 使用 $interview-slice-workflow，先读详细规则和实现验收表，在我指定的位置初始化独立工程，先检查并复用已有工具、字体和模型。媒体使用我指定的现有目录。完成自己的飞书授权后，按我提供的文档链接、批次编号和高清原片制作完整切片；需要的辅助镜头直接落实到视频，最终给可播放视频和交付文件夹入口。

## 内容入口

- [技能入口](skills/interview-slice-workflow/SKILL.md)
- [18组96条详细规则](skills/interview-slice-workflow/references/production-rules.md)
- [实现与验收矩阵](skills/interview-slice-workflow/references/implementation-matrix.md)
- [默认与覆盖](skills/interview-slice-workflow/references/defaults-and-overrides.md)
- [提炼方法及资讯Skill返工教训](skills/interview-slice-workflow/references/extraction-method.md)
- [当前验证记录](VALIDATION.md)
- [发布流程](PUBLISHING.md)

原声默认一次1.1倍、保持音高；封面精确3帧；双语完整意群字幕连续；大字提炼阶段核心思想；辅助镜头主动安排；批次差异不止颜色；已确认音乐不因改画面被替换；每有效分支保留最新。4:3/近1:1通常优先，全屏/原片条/字体/音乐按当前要求配置。

## 包含什么

可运行独立Remotion工程与锁文件，两种用于功能演示的构图，分段原声时间映射、字幕/SRT、语义字柔滑、辅助镜头、导入alpha、条件PiP/弹幕、字体实际文件校验、FFmpeg预处理/避让混音、实际编码核验、精确临时清理工具。官方飞书CLI和素材采集层复用MIT资讯包，用户自行授权；可使用已有连接器。

模板演示不是已获认可的真实访谈样片。复杂全屏裁剪、原生下条分离、人物抠图、语义选材、专业排版和音乐选择仍要操作者依据规则完成。没有内置ASR、人物分割模型、全自动抖音高规格案例采集、剪映转换或免授权素材库。

依赖先检查；标准安装Node 20.19/22.12+、Python 3.12+、FFmpeg/FFprobe、兼容Chrome。可显式复用已有兼容环境，不复制到每个项目。外盘只存媒体，工具/代码留适合的本机文件系统。机器路径在runtime.local.json，不进分发包。

代码MIT；依赖、字体和素材各自许可独立。仓库不含客户文稿、真实访谈、商业字体、音乐库或凭据。升级技能不会自动修改既有工程，需先做迁移差异检查。
