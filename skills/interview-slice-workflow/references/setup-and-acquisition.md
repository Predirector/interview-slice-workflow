# 首次配置、接入与媒体

## 可执行链路

```bash
python3 "$SKILL_DIR/scripts/init_project.py" /new/code --media-root /existing/media/batch
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code doctor
python3 /new/code/scripts/project.py setup --install
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code setup-acquisition
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code connect --configure
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code connect
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code status
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code intake --url https://example.feishu.cn/wiki/TOKEN --item 01 --section 第二批 --download
```

先doctor清点；setup --install明确执行独立锁定安装，不覆盖不兼容共享环境。复用已有工具时在runtime.local.json设置 nodeModules、python、ffmpeg、ffprobe、browserExecutable；机器专属配置不提交。可用安装位置由操作者检查填入，包不带作者路径。运行渲染时Node脚本解析指定nodeModules，不要求把依赖复制到项目。标准独立安装用npm ci，Python使用本项目venv；既有兼容环境优先复用，版本需报告。

媒体根目录必须已经存在且可写。初始化不会创建外盘挂载点，也不在外盘缺失时创建一个同名普通目录。public、deliverables、qa在媒体根；reports和代码在工程。明确媒体根才允许生成媒体，不能用默认fallback掩盖盘未挂。

## 飞书与资料读取

优先现有连接器；本包带官方CLI适配，接入层来自已验证资讯包。官方CLI管理登录和刷新，使用者自行完成首次应用配置、设备授权和文档权限，凭据不进JSON报告。安装不保证跨租户授权。

支持Docx/Wiki/Sheets与分页；编号匹配与原表格行/表头一起保留，重复编号用section选择，仍歧义就列出真实候选。附件只下载选中条目，不把整份文档全拉下。失败、过期、权限不足不能解释为无内容。原文保持与编辑理解并存，来源token、私有附件URL不公开。

收片后优先核对用户指定高清源；低清附件只作脚本匹配或定位。原片完整文件和源时间要证明一致，不可直接把低清源切点无偏移套高清MOV。

## 补采

```bash
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code search 'battery factory production official' --provider commons
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code fetch https://public.example/video --kind video --height 1080
python3 "$SKILL_DIR/scripts/slice.py" --project /new/code import /provided/source.mov
```

免费Commons/公开视频搜索可用；精确新闻和高规格账号搜索仍可使用当前环境网络搜索或用户资料。yt-dlp不保证抖音、B站等所有页面可提取，也不保证1080P。报告实际高度，降级不能伪称高清。浏览器Cookie仅经明确授权再加 --browser chrome；默认无Cookie。它可能读取该浏览器Cookie库，不能声称技术上只读一个域名；如授权仅允许单域名，应先用能真正限定域名的导出/接口，不传此选项。

下载记录不能自动授予使用许可或证明画面身份。每个候选人工核实后填sources及镜头用途；无法合法取得就换真实素材或说明缺口。网页截图保存真实版面，不重排冒充原报道。公众号专项坐标高亮并未随此包实现；不要把通用截图命令称作已完整覆盖所有公众号。

本包复用的采集器临时下载在project/reports生成，使用外盘工作流时将SLICE_ACQUISITION_TEMP设为存在的外盘临时目录；否则大视频不应调用下载。收件/下载前检查实际目标，不在内盘意外写大文件。
