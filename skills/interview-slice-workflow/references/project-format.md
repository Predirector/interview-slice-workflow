# 工程配置与命令契约

## 文件与路径

代码工程：AGENTS.md、PRODUCTION_RULES.md、IMPLEMENTATION_MATRIX.md、references/、episode.json、package.json及锁、requirements.txt、scripts/、src/、reports/。机器专属runtime.local.json忽略提交。初始化复制完整规则，项目独立于Skill安装目录。

媒体目录：public/（fonts、原片、prepared等）、deliverables/、qa/。public内文件使用相对路径；不允许绝对asset或..逃逸。稳定原件可通过本机有权限的导入归库，当前导入会复制文件，不会删除提供者原件。大型共享MOV如要避免复制，可显式建立适合本机构建器的引用并验证；不要把默认导入命令说成零复制。

## episode.json主要字段

|字段|意义|
|---|---|
|demo|功能演示=true；正式片必须false，核验采访语境与计划|
|width/height/fps/coverFrames|起始模板1080/1920/30/3；改变尺寸需同时适配组件与校验|
|speed|原声单次速度，默认1.1；变更需全时间线重建|
|source|public内原片文件|
|edits|按脚本顺序的sourceStart/sourceEnd秒，可选固定crop=[x,y,w,h]；同机位固定几何|
|title/titleLines/titleSize|完整文件标题、正文标题分行、实际字号；封面独立cover.titleLines/titleSize|
|style/frameMode/mediaBox|视觉系统、framed/full、[x,y,w,h]；无框全屏需操作者重新适配安全布局|
|interview|name/role/context/verified；上下文核验不是自动判断|
|fonts|title/semantic/caption分别file/weight/sha256|
|captions|正文帧start/end、zh/en、可选zhHighlights；完整连续无停顿标点|
|semantic|正文start/end与items：text/x/y/size；分组语义和重心由操作者判断|
|broll|start/end正文帧、file、sourceStart秒、rate、purpose、sourceIdentity、internalCuts（源秒列表，空数组表示人工核查无切镜，null表示未核查）|
|pip|正文start/end、box；原声讲话视频按正文全局时钟播放|
|foreground|public内已按正文时钟预处理、和底片几何相同的可用alpha视频；不做自动抠图|
|danmaku|start/duration正文帧、y/text/size；prepare测真实文字宽度|
|faces|每机位正文start/end、映射后的box，提示semantic面部矩形相交；不自动识别人脸|
|music|file、sourceStart、gain、title/author/license/sourceUrl等来源信息；null仅功能demo或经明确适配覆盖|
|branches|id、danmaku布尔；有效分支各留最新；当前模板只演示弹幕开关差异|
|stages/sources/overrides/retainedFiles|语义工作单、来源、规则覆盖、明确保留路径|

## 命令

- doctor：只读清点，写reports/doctor.json；不自动安装。
- setup --install：检查后安装缺失锁定依赖/官方默认字体。不覆写共享不兼容node_modules。显式配置已有Python时使用该解释器执行命令；新venv安装后用其Python继续。
- demo：只允许demo=true生成合成测试图和测试声，不能覆盖正式原片。
- font-import：合法字库绑定、复制校验、更新episode；不改变系统字体。
- validate：字体、时间映射、字幕、素材与候选问题报告；warning需要实际判断。
- prepare：生成单次提速人物、独立速度素材、静音三帧补偿混音、封面源帧和双语SRT，输出src/episode.compiled.json。
- node scripts/render.mjs plain / discussion：渲染对应完整分支；--cover输出封面；`plain --still 51`输出正文实际静帧；`plain --frames 120-150`内部复渲覆盖该效果段，不是完整成片。检查输出放qa。
- verify --branch plain：读实际MP4完整解码、帧数/声轨和精确三帧封面检查。
- cleanup-plan / cleanup：只为qa普通临时文件生成精确哈希计划与执行；清理后需实际复渲，不自动宣称完成。

标准执行顺序：doctor→配置/安装→写真实计划→validate→prepare→cover→完整分支→verify→人工审片→交付→授权范围清理→复渲→移除复渲过程件。对已有工程升级必须另做差异计划，初始化拒绝覆盖。
