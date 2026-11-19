# 逐项实现与验收矩阵

规则要求不等于工具全自动实现。组内每个细项按详细规则检查；下面标清现有入口和能力边界。正式审片记录必须绑定实际文件/时间/证据，不接受只有passed。

|规则组|实现入口|自动可检查|需要判断或未实现|
|---|---|---|---|
|R01|init_project.py；episode.overrides/branches|编号歧义；非demo正式校验|引语/权限/适用范围判断|
|R02|project.py doctor；common.py；sources清单|目录/可写性/工具/素材SHA|高清版本匹配、原片损失|
|R03|episode.interview；sources；review记录|必填采访语境与身份|媒体身份、原话限定核实|
|R04|timeline.py；project.py prepare|分段映射、整数帧、音画长度|音节、开场吸引力；独立视觉长镜需配置|
|R05|episode.mediaBox；Root.tsx Media|框比例/faceBox碰撞候选|居中、源信息条分离裁剪；未自动检测|
|R06|Root.tsx两构图；libraries.md|配置选择、样式可渲染|审美/空间深度/批次实质差异|
|R07|project.py font-import/validate；fonts.py|真实SHA/字重/字形/测量|笔画质感；商业字体由用户提供|
|R08|semantic数组；Root.tsx Semantic|区间/文本框与脸冲突|核心思想与承接；需外部合格alpha|
|R09|caption校验；SRT导出；Caption/Identity|双语连续、停顿标点、单行宽度|译文/阅读速度/姓名归属|
|R10|broll数组；prepare；MediaTimeline|源长度、整数帧、短回人物候选|身份/语义/许可/内部切镜需登记审看|
|R11|PiP/Alpha/Danmaku组件|真实文字宽度和全幅轨迹|弹幕讨论性/分割边缘；无内置分割模型|
|R12|music输入；prepare duck/mix|源/混音SHA、音轨存在/峰值|选曲与听感；无自动版权和情绪认证|
|R13|Cover组件；render cover；verify|3帧实际比较+第4帧、标题尺寸|采访语境真实性/第一注意点|
|R14|validate/verify；review样表|实际完整解码、帧数、哈希|人工项必须实际审看，不接受裸通过|
|R15|render.mjs命名；交付协议|输出文件/封面/字幕/报告|客户端播放器和入口实际可点|
|R16|cleanup-plan/cleanup；依赖列表|仅qa临时件、哈希重检、保留路径|其他旧交付清理与完整依赖审查由操作者；复渲必做|
|R17|libraries.md；defaults-and-overrides.md|配置中分离视觉/包装字段|高规格账号选例与组合质量，未自动采集抖音库|
|R18|独立初始化；锁文件；CLI接入层|格式/本地安装/初始化行为测试|账号首次授权、跨租户/所有平台未保证|

工具的输入契约见project-format.md，独立实测范围见仓库VALIDATION.md。没有验证记录的能力不声称已在另一台电脑或公网运行。
