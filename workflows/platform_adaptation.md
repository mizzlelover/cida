# Workflow F：平台适配（platform_adaptation）

同一篇内容，适配不同发布平台。**Platform Adapter 只调整呈现层，不改写底层语言理论。**

## 适配流程

1. 先完成内容本身的优化（Workflow A/B/C/D 任一）；
2. 确认目标平台，读取 `platforms/<平台>/README.md` 的专项参数；
3. 按平台参数调整：段落长度、小标题密度、开头速度、语域偏移、排版约定；
4. 检查：适配后的文本单独读，依然成立（不为平台牺牲逻辑与判断）。

## 平台速查

| 平台 | 目录 | 核心调整 |
|---|---|---|
| 通用 | `platforms/generic/` | 默认 Profile，屏幕阅读节奏 |
| 微信公众号 | `platforms/wechat/` | 移动端长文：段落短、小标题导航、读完率优先 |
| 小红书 | `platforms/xiaohongshu/` | 更高对话感、快速切入、强具体性、短块 |
| 知乎 | `platforms/zhihu/` | 论证、证据、解释密度优先 |
| 微博长文 | `platforms/weibo/` | 注意力稀缺环境，前置结论 |
| 视频口播稿 | `platforms/video_script/` | 口语节奏、呼吸、可发音性、听觉记忆 |
| 播客稿 | `platforms/podcast/` | 长程听觉跟随、话题回环 |

## 媒介声明（Mode Declaration）

每篇产出内部标注媒介模式，不同模式不同规则：

```
ARTICLE      屏幕阅读的文章
SPEECH       准备型演讲（scripted）
SCRIPT       视频/直播口播脚本
PODCAST      播客（半准备对话）
INTERVIEW    访谈
SOCIAL_POST  社交媒体
```

## 反平台腔

警惕各平台的工业腔，它们同样是模板：

- 公众号的"震惊体"开头与强行升华；
- 小红书的"姐妹们"式套近乎（Fake Intimacy）；
- 知乎的"谢邀"式自我包装残留；
- 口播稿的书面腔（写着顺口、念着拗口）。

平台适配 = **尊重读者的阅读情境**，不是套用该平台的流量模板。
