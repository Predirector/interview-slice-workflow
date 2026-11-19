# 视觉与字库的落实

## 制作次序

先用原片代表机位制作：封面、第一屏、提炼字最密屏、辅助镜头屏、结尾五类关键帧；缩至手机宽度比较。检查标题是否是第一注意点、人物占比、字组重心、边缘和背景深度，再做动效。模板只是功能起点，不是审美授权。

两种起始构图：

- studio-amber：深墨纹理、暖色主字、有承托阴影的4:3主框；名字条在主框下缘偏左，提炼组靠近下部人物。配合横向柔滑。
- editorial-teal：偏冷环境层次与下缘过渡，人物主框更靠上；姓名为胸前窄竖块，提炼组以错层叠置建立重心，入场以纵向轻位移加淡入。颜色之外容器、坐标、阶段字布局和进入方向不同。

两种都不是固定账户模板。需要真正全屏时改mediaBox与title/caption/face区域并审片；不要仅拉伸视频。实际无框全屏及原生条分离适配需要操作者按原片修改crop/preparation，本包未自动识别原片信息条。

## 真字体

```bash
python3 scripts/project.py font-import --role title --file /licensed/heavy-sans.ttf --weight 900
python3 scripts/project.py font-import --role semantic --file /licensed/heavy-song.ttf --weight 400
python3 scripts/project.py font-import --role caption --file /licensed/bold-sans.ttf --weight 700
python3 scripts/project.py validate
```

支持TTF/OTF的fontTools检查；TTC应先在许可允许范围导出合法单face并记录，当前工具不自动拆TTC。每角色独立file/weight/sha256/family，固定文件与字形，不读操作系统同名字体。可变字体报告实际axis范围，配置字重必须有效。名称里有Bold不一定粗，元数据Regular不一定细；非可变字体与选用weight明显不符时失败，若设计字库元数据特殊须手动核实再扩展工具，不能自动伪粗。

默认Noto Sans SC是公开许可演示字库，固定官方下载SHA；有厚宋要求时需使用者实际提供，不会将Noto冒称方正。全字形覆盖测试包括封面、标题、提炼组、字幕、身份、弹幕和必要图注；缺字停止，不能悄悄从系统fallback。前景文字应清楚关闭font-synthesis，等待document.fonts.load与ready。

手机图需能看到笔画饱满度、全句完整与层级。固定坐标不说明匀称，实际text metrics用于宽度，字组与人整体重心人工看；过长字幕先拆时段。标题和封面不强制同坐标字号。

## 背景与前景

背景可叠柔光、纹理和远近轮廓，适度微动，避开尖锐PPT装饰。主框用轻阴影与边缘分离。前景alpha必须与底片使用相同时间映射和几何，不能对一层二次提速。mask在头发/手/镜头切换逐帧看，没可用分割不要假装成功。纯装饰文本尽量放身体附近，保持脸和话筒无损；validate的faceBox碰撞只能提示文字框，不能替代查看真实透明轮廓。

## 可视基线

assets/visual-baselines提供这次实际渲染的手机静帧/动态示例说明（如有）。它只证明功能演示已看，不代表真实访谈质量，也不替代稿件适配。基线更新要包含源配置、字体SHA、帧号及真实查看结论，不能只贴一张无来源美图。
