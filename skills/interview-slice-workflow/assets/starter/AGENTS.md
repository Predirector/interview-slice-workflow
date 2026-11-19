# 访谈切片工程

制作/修改前读取 PRODUCTION_RULES.md、IMPLEMENTATION_MATRIX.md 与 references/defaults-and-overrides.md。规则随项目复制，不依赖原Skill安装路径。用户当前要求优先；不要把demo写成正式任务。

工程配置 episode.json；机器/媒体位置 runtime.local.json（不提交）。运行 python3 scripts/project.py doctor、setup --install、demo、validate、prepare、node scripts/render.mjs、verify。先检查并复用环境，媒体目录缺失停止。必要时按当前规范补齐真实原片/字体/音乐/字幕，不能自动拿合成演示交付。

输出使用原标题。每个有效分支保留最新，生成后提供本地播放器和交付文件夹。清理范围与权限由本项目/用户明确，不因本Skill存在自动获全盘删除许可。清理后实际渲染对应效果片段并解码。
