# HQ ICON · App Store 高清图标下载器

高质量 App Store 图标下载器，参考 [icon.yukonga.top](https://icon.yukonga.top/) 实现。基于 [Apple iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)，纯前端、无后端、无密钥，可直接部署到 GitHub Pages。

**在线地址：https://iosyyds.github.io/hq-icon/**（仓库 Settings → Pages 开启后即可访问）

## 功能特性

- 平台：iOS / iPadOS / macOS
- 地区：17 个 App Store 地区（CN / US / JP / KR / TW / HK / SG / GB / FR / DE / IT / ES / RU / IN / TH / ID / PH）
- 样式：官方 / 常规 / 圆角 / 原始（预览遮罩）
- 格式：JPEG / PNG / WebP
- 尺寸：256 / 512 / 1024 px
- 一键下载，文件名自动命名（App名-尺寸.格式）
- 深色主题、响应式布局

## 本地运行

直接双击打开 `index.html` 即可，或启动本地服务：

```bash
python3 -m http.server 8080
# 访问 http://localhost:8080
```

## 部署到 GitHub Pages

1. 将代码推送到 GitHub 仓库（例如 `hq-icon`）
2. 仓库 Settings → Pages → Source 选择 `Deploy from a branch` → 分支 `main`，目录 `/ (root)` → Save
3. 等待 1~2 分钟，访问 `https://<用户名>.github.io/hq-icon/`

## 技术说明

- 搜索接口：`https://itunes.apple.com/search`，`entity` 按平台切换 `software` / `ipadSoftware` / `macSoftware`
- 图标转换：直接改写 mzstatic 图片 URL 的尺寸与扩展名（`/512x512bb.jpg` → `/1024x1024bb.webp`），零服务端转换
- 下载：fetch → blob → `a[download]`，失败时自动回退到新窗口打开原图
- 数据来自 Apple iTunes Search API，图标版权归各应用开发者所有，本工具仅供个人学习使用

## License

MIT
