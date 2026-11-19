---
name: interview-slice-workflow
description: 将真实访谈、演讲和原声素材剪辑包装成竖屏切片，处理脚本取舍、高清原片、双语字幕、语义大字、辅助镜头、封面、配乐及多分支交付。适用于制作或修改讲话切片，不用于从零生成数字人或纯字幕资讯。
---
# 访谈切片工作流

把已有真实原声制作成可编辑、可核验的完整视频。先判断稿件和画面，不把一个期次的样式当所有账号模板。普通制作连续完成；只有用户要求先审方向时停在预览。

## 先读、再判定

- 首次制作、提炼规则、跨机复现：完整读 [详细制作规则](references/production-rules.md)、[实现与验收矩阵](references/implementation-matrix.md)。这两份不是可跳过的摘要。
- 识别旧要求冲突、修改既有片：[默认与覆盖](references/defaults-and-overrides.md)。原话顺序跟脚本，默认一次1.1倍，封面精确3帧；1.2倍、全屏、圆框、宋体、弱配乐均有各自作用范围。
- 环境和飞书素材：[首次配置与接入](references/setup-and-acquisition.md)。不假设作者账号、工具、外盘或字体可用。先核对目录和已有环境。
- 画面/封面/字库：[视觉与字体](references/visual-and-fonts.md)。先解决构图、字体、层级和背景，再加动画。封面更大更清楚、交代已核实采访语境，无对白字幕。
- 剪辑/字幕/辅助镜头：[时间线与镜头](references/timeline-and-broll.md)；输入配置见 [工程数据](references/project-format.md)。所有时钟、语义安排和实际源切镜都要明确。
- 人像层次/PiP/弹幕：[包装组件](references/packaging.md)。只有可用能力才实施，无法完成动态抠图不能冒称完成。
- 选曲和听感：[声音](references/audio.md)；完成前读 [审片与交付](references/review-and-delivery.md) 和 [清理](references/cleanup.md)。
- 丰富可组合视觉/包装库：[案例与组合](references/libraries.md)。不能拿功能演示当审美标准。

## 可运行入口

以本SKILL所在目录为SKILL_DIR，不写死安装路径：

```bash
python3 "$SKILL_DIR/scripts/init_project.py" /path/to/new-project --media-root /existing/writable/media/project
python3 "$SKILL_DIR/scripts/slice.py" --project /path/to/new-project doctor
python3 /path/to/new-project/scripts/project.py setup --install
```

本包提供独立锁文件、两套演示构图、3帧封面、原声分段变速、双语连续字幕、阶段字、辅助镜头、外部alpha、条件PiP和弹幕、字体/计划校验、实际编码核验、显式清理计划与复渲入口。`setup --install`前先doctor；可在runtime.local.json指定已有本机工具，不能盲装重复环境。

正式制作：读脚本并定位唯一条目→检查高清原片→逐阶段写原话/核心命题/人物或辅助镜头→形成源与输出时间映射→确定当前视觉与封面→准备并校验字体/媒体/混音→内部静帧和手机审看→完整导出及实际编码审片→发布当前交付入口→在已授权范围同轮清理、复渲。

初始化只创建新目录，更新不覆盖已有工程。模板只演示功能，正式任务必须替换demo配置、核实原话与素材、记录人工验收。不能拿默认排版承诺原样复现，不能把程序通过当审美或听感通过。

## 必守交付边界

每有效分支保留最新交付，用户要求保留的历史文件例外。三帧封面后立即动态正文；字幕连续、双语、无停顿标点；素材落实到视频，不止搜集页；同批不同曲目；实际查看脸、文字和素材切点。

支持本地播放器的客户端使用 `![原标题](/absolute/path/原标题.mp4)`，旁边附 `[打开交付文件夹](/absolute/path/deliverables)`。其他客户端用其原生媒体预览。清理不得扩大到唯一原件、其他项目或共享库。

接入、审美与未实现能力的边界必须按矩阵披露；不要自行上传客户内容或公开新仓库。规则维护方法及这次从资讯分发过程学到的教训见 [提炼方法](references/extraction-method.md)。
