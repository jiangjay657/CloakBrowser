# CloakBrowser 中文说明

> 本文件由 AI 根据项目 `README.md` 翻译整理，便于中文阅读。原始英文版请见 [`README.md`](README.md)。

## 项目简介

CloakBrowser 是一个“隐身版 Chromium”自动化浏览器项目，目标是在使用 Playwright / Puppeteer / Selenium 等自动化框架时，尽量避免被网站的机器人检测、浏览器指纹检测、无头浏览器检测和部分验证码风控系统识别。

它不是简单地修改 Playwright 配置，也不是在页面里注入 JavaScript，而是使用经过源码级 C++ 补丁修改并重新编译的 Chromium 浏览器二进制文件。项目提供 Python 与 JavaScript / TypeScript 两套封装，让你像使用 Playwright 或 Puppeteer 一样启动这个定制浏览器。

核心特点：

- 基于 Chromium 的定制浏览器二进制文件。
- 通过源码级补丁修改 Canvas、WebGL、Audio、字体、GPU、屏幕、WebRTC、网络时序、自动化信号、CDP 输入行为等指纹特征。
- 支持 Python、Node.js / TypeScript。
- 可作为 Playwright / Puppeteer 的替代启动器，代码迁移成本低。
- 支持代理，包括 HTTP 与 SOCKS5。
- 支持根据代理出口 IP 自动匹配时区与语言环境。
- 支持持久化浏览器 profile，用于保留 Cookie、localStorage、缓存等。
- 支持 `humanize=True`，自动把鼠标、键盘、滚动操作变得更像真人。
- 支持 Docker、CDP server 模式，以及多种爬虫 / AI Agent 框架集成。

> 注意：CloakBrowser 不负责“解验证码”，它的定位是尽量降低自动化浏览器被触发验证码或封禁的概率。使用时仍需遵守目标网站的服务条款、法律法规和授权边界。

---

## 快速体验

无需安装，可以直接用 Docker 测试：

```bash
docker run --rm cloakhq/cloakbrowser cloaktest
```

Python 示例：

```python
from cloakbrowser import launch

browser = launch()
page = browser.new_page()
page.goto("https://protected-site.com")
browser.close()
```

JavaScript / Playwright 示例：

```javascript
import { launch } from 'cloakbrowser';

const browser = await launch();
const page = await browser.newPage();
await page.goto('https://protected-site.com');
await browser.close();
```

Puppeteer 也支持：

```javascript
import { launch } from 'cloakbrowser/puppeteer';
```

---

## 安装

### Python

```bash
pip install cloakbrowser
```

首次运行时，会自动下载定制版 Chromium 二进制文件，大小约 200MB，并缓存到本地。

如果需要根据代理 IP 自动识别时区 / 语言环境：

```bash
pip install cloakbrowser[geoip]
```

### JavaScript / Node.js

使用 Playwright：

```bash
npm install cloakbrowser playwright-core
```

使用 Puppeteer：

```bash
npm install cloakbrowser puppeteer-core
```

---

## 从 Playwright 迁移

原 Playwright 代码：

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
browser = pw.chromium.launch()
```

改为 CloakBrowser：

```python
from cloakbrowser import launch
browser = launch()
```

后续 `page = browser.new_page()`、`page.goto()` 等 Playwright API 基本保持不变。

---

## Browser Profile Manager

项目还提到一个独立的浏览器配置文件管理器，可作为 Multilogin、GoLogin、AdsPower 的自托管替代方案，用于创建带有独立指纹、代理和持久会话的浏览器 profile，并通过 noVNC 在浏览器中操作。

启动方式：

```bash
docker run -p 8080:8080 -v cloakprofiles:/data cloakhq/cloakbrowser-manager
```

然后打开：

```text
http://localhost:8080
```

创建 profile 后点击 Launch 即可。

项目地址：<https://github.com/CloakHQ/CloakBrowser-Manager>

---

## 最新版本说明

README 中标注的版本为：

- CloakBrowser：v0.3.26
- Chromium：146.0.7680.177.x

主要更新点：

- 新增 `launch_context_async()`。
- JS 版本支持 `contextOptions`，可把任意参数传给 Playwright `newContext()`。
- 原生支持 SOCKS5 代理。
- 升级到 Chromium 146。
- 增加到 57 个指纹补丁，覆盖 WebAuthn、AAC Audio、窗口位置、WebGL / Canvas 一致性等。
- 支持 WebRTC IP 伪装。
- 清理代理相关泄漏信号，例如 DNS / connect / SSL timing、代理缓存头、`Proxy-Connection` 头。
- `cloakserve` 改写为多连接 CDP 代理，每个连接可使用不同指纹种子。
- 改进 `humanize=True` 的键盘事件隔离与可信派发。
- 默认无需额外参数即可随机生成指纹种子。
- 支持从代理 IP 自动推断时区与 locale。
- 支持持久化 profile。

---

## 为什么使用 CloakBrowser？

常见的 stealth 工具通常通过 JavaScript 注入或启动参数修补，例如：

- playwright-stealth
- undetected-chromedriver
- puppeteer-extra

这类方式的问题是：

- Chrome 更新后容易失效。
- 反机器人系统可能检测到“补丁本身”。
- 很多特征只能在表层修补，无法做到浏览器底层一致。

CloakBrowser 的做法是：

- 修改 Chromium 源码并重新编译。
- 在浏览器二进制层面处理指纹特征。
- 尽量让检测系统看到的是“真实浏览器行为”。
- 本地、Docker、VPS 上行为保持一致。
- 可与 browser-use、Crawl4AI、Scrapling、Stagehand、LangChain、Selenium 等框架集成。

---

## 测试结果概览

README 中列出的检测结果包括：

| 检测服务 | 普通 Playwright | CloakBrowser |
|---|---|---|
| reCAPTCHA v3 | 0.1，偏机器人 | 0.9，偏真人 |
| Cloudflare Turnstile 非交互 | 失败 | 通过 |
| Cloudflare Turnstile managed | 失败 | 通过 |
| ShieldSquare | 被拦截 | 通过 |
| FingerprintJS bot detection | 被检测 | 通过 |
| BrowserScan bot detection | 被检测 | NORMAL |
| navigator.webdriver | true | false |
| navigator.plugins.length | 0 | 5 |
| User-Agent | HeadlessChrome | Chrome/146 |
| TLS 指纹 | 不匹配 | 与 Chrome 匹配 |

这些结果来自项目作者对在线检测服务的测试。实际效果会受到 IP 信誉、代理质量、目标网站策略、浏览器模式、字体环境、行为模式等因素影响。

---

## 工作原理

CloakBrowser 是定制 Chromium 二进制文件外面的一层轻量封装：

1. 安装 Python 包或 npm 包。
2. 首次启动时自动下载适合当前平台的定制 Chromium。
3. 运行时通过 Playwright 或 Puppeteer 启动该定制二进制文件。
4. 你的业务代码继续使用标准 Playwright / Puppeteer API。

二进制文件包含源码级补丁，覆盖：

- Canvas
- WebGL
- Audio
- 字体
- GPU
- 屏幕属性
- WebRTC
- 网络时序
- 硬件信息
- 自动化信号移除
- CDP 输入行为模拟

下载的二进制文件会通过 SHA-256 校验。

---

## Python API

### `launch()`

```python
from cloakbrowser import launch

# 基础启动：无头模式，默认隐身配置
browser = launch()

# 有头模式：显示浏览器窗口
browser = launch(headless=False)

# 使用 HTTP 或 SOCKS5 代理
browser = launch(proxy="http://user:pass@proxy:8080")
browser = launch(proxy="socks5://user:pass@proxy:1080")

# 使用 Playwright 风格代理字典
browser = launch(proxy={
    "server": "http://proxy:8080",
    "bypass": ".google.com",
    "username": "user",
    "password": "pass",
})

# 额外 Chrome 参数
browser = launch(args=["--disable-gpu"])

# 设置时区与语言环境
browser = launch(timezone="America/New_York", locale="en-US")

# 根据代理 IP 自动检测时区 / locale，需要 cloakbrowser[geoip]
browser = launch(proxy="http://proxy:8080", geoip=True)

# 伪装 WebRTC IP
browser = launch(proxy="http://proxy:8080", args=["--fingerprint-webrtc-ip=auto"])

# 启用真人化鼠标、键盘、滚动行为
browser = launch(humanize=True)

# 使用更谨慎、更慢的真人化预设
browser = launch(humanize=True, human_preset="careful")

# 关闭默认 stealth 参数，自行传入指纹参数
browser = launch(stealth_args=False, args=["--fingerprint=12345"])
```

返回值是 Playwright 的 `Browser` 对象，可继续使用：

- `new_page()`
- `new_context()`
- `close()`
- 其他 Playwright API

### `launch_async()`

异步版本：

```python
import asyncio
from cloakbrowser import launch_async

async def main():
    browser = await launch_async()
    page = await browser.new_page()
    await page.goto("https://example.com")
    print(await page.title())
    await browser.close()

asyncio.run(main())
```

### `launch_context()`

一次性创建 browser + context：

```python
from cloakbrowser import launch_context

context = launch_context(
    user_agent="Custom UA",
    viewport={"width": 1920, "height": 1080},
    locale="en-US",
    timezone="America/New_York",
)
page = context.new_page()
page.goto("https://protected-site.com")
context.close()
```

额外参数会转发给 Playwright 的 `browser.new_context()`，例如：

- `storage_state`
- `permissions`
- `extra_http_headers`

保存 / 恢复会话示例：

```python
from cloakbrowser import launch_context

context = launch_context(storage_state="state.json")
page = context.new_page()
page.goto("https://example.com")
context.storage_state(path="state.json")
context.close()
```

### `launch_context_async()`

异步版本：

```python
import asyncio
from cloakbrowser import launch_context_async

async def main():
    ctx = await launch_context_async(storage_state="state.json")
    page = await ctx.new_page()
    await page.goto("https://example.com")
    await ctx.storage_state(path="state.json")
    await ctx.close()

asyncio.run(main())
```

### `launch_persistent_context()`

使用持久化用户目录，Cookie、localStorage、缓存等会跨会话保留。

适用场景：

- 保持登录状态。
- 避免网站检测隐身 / 私密浏览模式。
- 加载 Chrome 扩展。
- 累积自然浏览历史、缓存、Service Worker、IndexedDB 等。

示例：

```python
from cloakbrowser import launch_persistent_context

ctx = launch_persistent_context("./my-profile", headless=False)
page = ctx.new_page()
page.goto("https://protected-site.com")
ctx.close()

# 下次继续使用同一 profile
ctx = launch_persistent_context("./my-profile", headless=False)
```

异步版本：`launch_persistent_context_async()`。

---

## 命令行工具

```bash
python -m cloakbrowser install      # 预下载浏览器二进制文件
python -m cloakbrowser info         # 显示版本、路径、平台信息
python -m cloakbrowser update       # 检查并下载新版二进制文件
python -m cloakbrowser clear-cache  # 清理缓存的二进制文件
```

实用函数：

```python
from cloakbrowser import binary_info, clear_cache, ensure_binary

print(binary_info())
clear_cache()
ensure_binary()
```

---

## JavaScript / Node.js API

### Playwright

```javascript
import { launch, launchContext, launchPersistentContext } from 'cloakbrowser';

const browser = await launch();

const browser2 = await launch({
  headless: false,
  proxy: 'http://user:pass@proxy:8080',
  args: ['--fingerprint=12345'],
  timezone: 'America/New_York',
  locale: 'en-US',
  humanize: true,
});

const context = await launchContext({
  userAgent: 'Custom UA',
  viewport: { width: 1920, height: 1080 },
  locale: 'en-US',
  timezone: 'America/New_York',
});
const page = await context.newPage();

const ctx = await launchPersistentContext({
  userDataDir: './chrome-profile',
  headless: false,
  proxy: 'http://user:pass@proxy:8080',
});
```

### Puppeteer

项目建议：对 reCAPTCHA Enterprise 等敏感场景，优先用 Playwright，因为 Puppeteer 的 CDP 流量更容易暴露自动化信号。

```javascript
import { launch } from 'cloakbrowser/puppeteer';

const browser = await launch({ headless: true });
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

### JS 实用函数

```javascript
import { ensureBinary, clearCache, binaryInfo } from 'cloakbrowser';

await ensureBinary();
console.log(binaryInfo());
clearCache();
```

---

## 真人行为模拟：`humanize=True`

启用后，鼠标、键盘、滚动等交互会被自动替换成更接近真人的行为。

Python：

```python
browser = launch(humanize=True)
page = browser.new_page()
page.goto("https://example.com")
page.locator("#email").fill("user@example.com")
page.locator("button[type=submit]").click()
```

JavaScript：

```javascript
import { launch } from 'cloakbrowser';
const browser = await launch({ humanize: true });
```

变化包括：

| 行为 | 默认自动化 | `humanize=True` |
|---|---|---|
| 鼠标移动 | 瞬移 | 贝塞尔曲线、缓动、轻微过冲 |
| 点击 | 瞬间点击 | 真实瞄准点、按住时长 |
| 键盘 | 瞬间填值 | 逐字符输入、思考停顿、偶尔打错再修正 |
| 滚动 | 跳跃 | 加速、匀速、减速的微步滚动 |
| `fill()` | 直接设置值 | 先清空再逐字输入 |

预设：

```python
browser = launch(humanize=True, human_preset="careful")
```

```javascript
const browser = await launch({ humanize: true, humanPreset: 'careful' });
```

自定义配置：

```python
browser = launch(humanize=True, human_config={
    "mistype_chance": 0.05,
    "typing_delay": 100,
    "idle_between_actions": True,
    "idle_between_duration": [0.3, 0.8],
})
```

```javascript
const browser = await launch({
    humanize: true,
    humanConfig: {
        mistype_chance: 0.05,
        typing_delay: 100,
        idle_between_actions: true,
        idle_between_duration: [0.3, 0.8],
    }
});
```

注意：Playwright 中建议使用 `page.click(selector)`、`page.type(selector, text)`、`page.hover(selector)` 或 Locator API，避免直接 `page.query_selector()` 后操作 ElementHandle，否则可能绕过 humanize 补丁。

---

## 环境变量配置

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `CLOAKBROWSER_BINARY_PATH` | 无 | 跳过下载，使用本地 Chromium 二进制文件 |
| `CLOAKBROWSER_CACHE_DIR` | `~/.cloakbrowser` | 二进制缓存目录 |
| `CLOAKBROWSER_DOWNLOAD_URL` | `cloakbrowser.dev` | 自定义二进制下载地址 |
| `CLOAKBROWSER_AUTO_UPDATE` | `true` | 是否启用后台更新检查 |
| `CLOAKBROWSER_SKIP_CHECKSUM` | `false` | 是否跳过 SHA-256 校验 |
| `CLOAKBROWSER_GEOIP_TIMEOUT_SECONDS` | `5` | GeoIP 解析最大等待秒数 |

---

## 指纹管理

默认情况下，二进制文件会在启动时自动生成随机指纹种子，并根据种子生成一致的浏览器身份，包括：

- GPU
- 硬件并发数
- 设备内存
- 屏幕尺寸
- Canvas 噪声
- WebGL 噪声
- Audio 噪声
- 字体相关特征

常见场景：

| 场景 | 行为 |
|---|---|
| 不传参数 | 每次启动自动生成随机指纹 |
| `--fingerprint=seed` | 使用固定种子，跨会话保持同一设备身份 |
| 固定种子 + 显式参数 | 显式参数覆盖自动生成值，其余由种子生成 |

如果你频繁访问同一网站，建议使用固定种子，让同一个 IP / 会话看起来像同一台回访设备：

```python
browser = launch(args=["--fingerprint=12345"])
```

```javascript
const browser = await launch({ args: ['--fingerprint=12345'] });
```

默认指纹参数：

| 参数 | Linux/Windows 默认 | macOS 默认 | 控制内容 |
|---|---|---|---|
| `--fingerprint` | 随机 | 随机 | Canvas、WebGL、Audio、字体、Client Rects 的主种子 |
| `--fingerprint-platform` | `windows` | `macos` | `navigator.platform`、UA 操作系统、GPU 池 |

可选额外参数包括：

- `--fingerprint-gpu-vendor`
- `--fingerprint-gpu-renderer`
- `--fingerprint-hardware-concurrency`
- `--fingerprint-device-memory`
- `--fingerprint-screen-width`
- `--fingerprint-screen-height`
- `--fingerprint-brand`
- `--fingerprint-brand-version`
- `--fingerprint-platform-version`
- `--fingerprint-location`
- `--fingerprint-timezone`
- `--fingerprint-locale`
- `--fingerprint-storage-quota`
- `--fingerprint-taskbar-height`
- `--fingerprint-fonts-dir`
- `--fingerprint-webrtc-ip`
- `--fingerprint-noise=false`
- `--enable-blink-features=FakeShadowRoot`

更改这些参数可能影响检测结果，建议先测试。

---

## Linux 字体设置

在 Kasada、Akamai 等强检测网站上，Linux 最小化环境缺少字体可能导致 Canvas emoji 渲染哈希异常，从而被识别。

推荐安装：

```bash
sudo apt install -y fonts-noto-color-emoji fonts-freefont-ttf fonts-unifont \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-tlwg-loma-otf
```

官方 Docker 镜像已内置这些字体。

如果需要更接近 Windows 字体枚举，可从 Windows 机器复制 `C:\Windows\Fonts\` 下的字体：

```bash
mkdir -p ~/.local/share/fonts/windows
cp /path/to/windows/fonts/*.ttf ~/.local/share/fonts/windows/
cp /path/to/windows/fonts/*.TTF ~/.local/share/fonts/windows/
fc-cache -f
```

然后启动时指定：

```python
browser = launch(
    args=["--fingerprint-fonts-dir=/home/user/.local/share/fonts/windows"],
)
```

---

## 示例文件

Python 示例在 [`examples/`](examples/)：

- `basic.py`：启动并加载页面。
- `persistent_context.py`：持久化 profile。
- `recaptcha_score.py`：检测 reCAPTCHA v3 分数。
- `stealth_test.py`：运行多个检测网站测试。
- `fingerprint_scan_test.py`：测试 fingerprint-scan.com 和 CreepJS。

JavaScript 示例在 [`js/examples/`](js/examples/)：

- `basic-playwright.ts`
- `basic-puppeteer.ts`
- `persistent-context.ts`
- `stagehand.ts`
- `stealth-test.ts`

---

## 框架集成

CloakBrowser 可与任何使用 Playwright 或 Chromium 的框架配合。

方式一：让框架直接启动 CloakBrowser 的二进制文件：

```python
from cloakbrowser.download import ensure_binary
from cloakbrowser.config import get_default_stealth_args

binary_path = ensure_binary()
stealth_args = get_default_stealth_args()
```

方式二：先启动 CloakBrowser，再让框架通过 CDP 连接：

```python
from cloakbrowser import launch_async

browser = await launch_async(args=["--remote-debugging-port=9242"])
# 让框架连接 http://127.0.0.1:9242
```

README 中列出的集成包括：

- browser-use
- Crawl4AI
- Crawlee
- Scrapling
- Stagehand
- LangChain
- Selenium
- undetected-chromedriver
- agent-browser
- AWS Lambda

---

## 支持平台

| 平台 | Chromium | 补丁数 | 状态 |
|---|---|---|---|
| Linux x86_64 | 146 | 57 | 支持 |
| Linux arm64 | 146 | 57 | 支持 |
| macOS arm64 | 145 | 26 | 支持 |
| macOS x86_64 | 145 | 26 | 支持 |
| Windows x86_64 | 146 | 57 | 支持 |

包装器会自动下载适合当前平台的二进制文件。

macOS 首次运行时可能被 Gatekeeper 阻止，需要右键应用，选择 Open 并确认。

---

## Docker 使用

### 快速测试

```bash
docker run --rm cloakhq/cloakbrowser cloaktest
```

### 运行脚本

```bash
docker run --rm cloakhq/cloakbrowser python -c "
from cloakbrowser import launch
browser = launch()
page = browser.new_page()
page.goto('https://example.com')
print(page.title())
browser.close()
"
```

挂载自己的脚本：

```bash
docker run --rm -v ./my_script.py:/app/my_script.py cloakhq/cloakbrowser python my_script.py
```

使用代理：

```bash
docker run --rm cloakhq/cloakbrowser python -c "
from cloakbrowser import launch
browser = launch(proxy='http://user:pass@proxy:8080')
page = browser.new_page()
page.goto('https://example.com')
print(page.title())
browser.close()
"
```

### CDP server 模式

启动一个持久运行的 stealth 浏览器，并通过 Chrome DevTools Protocol 远程连接：

```bash
docker run -d --name cloak -p 127.0.0.1:9222:9222 cloakhq/cloakbrowser cloakserve
```

Python 连接示例：

```python
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
browser = pw.chromium.connect_over_cdp("http://localhost:9222")
page = browser.new_page()
page.goto("https://example.com")
print(page.title())
browser.close()
```

带代理启动：

```bash
docker run -d --name cloak -p 127.0.0.1:9222:9222 cloakhq/cloakbrowser \
  cloakserve --proxy-server=http://proxy:8080
```

有头模式：

```bash
docker run -d --name cloak -p 127.0.0.1:9222:9222 cloakhq/cloakbrowser \
  cloakserve --headless=false
```

停止：

```bash
docker stop cloak && docker rm cloak
```

安全提醒：CDP 端口拥有浏览器完全控制权，不要未经认证暴露到公网。

### Docker Compose

```yaml
services:
  cloakbrowser:
    image: cloakhq/cloakbrowser
    command: cloakserve
    restart: unless-stopped
    ports:
      - "127.0.0.1:9222:9222"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9222/json/version"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

### 多指纹连接

同一个 CDP 服务可通过查询参数为不同连接使用不同指纹种子：

```python
b1 = pw.chromium.connect_over_cdp("http://localhost:9222?fingerprint=11111")
b2 = pw.chromium.connect_over_cdp("http://localhost:9222?fingerprint=22222")

b3 = pw.chromium.connect_over_cdp(
    "http://localhost:9222?fingerprint=33333"
    "&timezone=Asia/Tokyo&locale=ja-JP&platform=macos"
    "&hardware-concurrency=4&device-memory=8"
)

b4 = pw.chromium.connect_over_cdp(
    "http://localhost:9222?fingerprint=44444"
    "&proxy=http://proxy:8080&geoip=true"
)
```

支持的查询参数包括：

- `fingerprint`
- `timezone`
- `locale`
- `platform`
- `platform-version`
- `brand`
- `brand-version`
- `gpu-vendor`
- `gpu-renderer`
- `hardware-concurrency`
- `device-memory`
- `screen-width`
- `screen-height`
- `proxy`
- `geoip`

### 持久化 profile

```bash
docker run --rm -v ./my-profile:/profile cloakhq/cloakbrowser python -c "
from cloakbrowser import launch_persistent_context
ctx = launch_persistent_context('/profile')
page = ctx.new_page()
page.goto('https://example.com')
ctx.close()
"
```

下次使用同一 volume，Cookie、localStorage、缓存会被恢复。

资源占用：空闲约 190MB RAM，3 个标签页约 280MB，每增加一个标签页约 30MB。

---

## 反机器人站点推荐配置

对强风控网站，README 推荐：

```python
browser = launch(
    proxy="http://your-residential-proxy:port",  # 住宅代理更稳，数据中心 IP 容易被信誉拦截
    geoip=True,       # 根据代理出口 IP 匹配时区和语言环境
    headless=False,   # 有头模式
    humanize=True,    # 真人化行为
)
```

JavaScript：

```javascript
const browser = await launch({
    proxy: 'http://your-residential-proxy:port',
    geoip: true,
    headless: false,
    humanize: true,
});
```

如代理支持 SOCKS5，优先使用 SOCKS5：

```python
browser = launch(proxy="socks5://user:pass@proxy:1080", geoip=True, headless=False, humanize=True)
```

---

## 常见问题排查

### DataDome / Turnstile 等仍被拦截

一些网站会检测无头模式，即使有 C++ 补丁也可能被识别。可在 Linux 上用 Xvfb 提供虚拟显示并使用有头模式：

```bash
sudo apt install xvfb
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

```python
from cloakbrowser import launch

browser = launch(headless=False, proxy="http://your-residential-proxy:port")
page = browser.new_page()
page.goto("https://heavily-protected-site.com")
browser.close()
```

### Kasada / Akamai 仍被拦截

检查 Linux 字体是否完整，尤其是 emoji 与扩展字体。缺字体会导致 Canvas 渲染哈希异常。

### 新会话被挑战，但访问一次后正常

使用持久化 profile 预热 Cookie：

```python
from cloakbrowser import launch_persistent_context

ctx = launch_persistent_context("./profile", args=["--disable-http2"])
page = ctx.new_page()
page.goto("https://example.com")
ctx.close()

ctx = launch_persistent_context("./profile")
page = ctx.new_page()
page.goto("https://example.com")
```

### 更新到最新版

```bash
pip install -U cloakbrowser
npm install cloakbrowser@latest
docker pull cloakhq/cloakbrowser:latest
```

### 二进制下载失败

可指定本地浏览器二进制：

```bash
export CLOAKBROWSER_BINARY_PATH=/path/to/your/chrome
```

### 回退版本

```bash
pip install cloakbrowser==0.3.21
npm install cloakbrowser@0.3.21
docker pull cloakhq/cloakbrowser:0.3.21
```

### macOS 提示 App 损坏或 Gatekeeper 阻止

```bash
xattr -cr ~/.cloakbrowser/chromium-*/Chromium.app
```

### 是否需要 `playwright install chromium`？

不需要。CloakBrowser 会下载自己的 Chromium。只需要 Playwright 系统依赖：

```bash
playwright install-deps chromium
```

### 网站检测隐身 / 私密模式

`launch()` 默认创建临时上下文，部分网站可能认为它像隐身模式。可以用：

```python
from cloakbrowser import launch_persistent_context
ctx = launch_persistent_context("./my-profile", headless=False)
```

### reCAPTCHA v3 分数低

避免使用 `page.wait_for_timeout()`，因为它会产生 CDP 命令：

```python
# 不推荐
page.wait_for_timeout(3000)

# 推荐
import time
time.sleep(3)
```

JavaScript：

```javascript
// 不推荐
await page.waitForTimeout(3000);

// 推荐
await new Promise(r => setTimeout(r, 3000));
```

其他建议：

- 尝试 Patchright 后端：`pip install cloakbrowser[patchright]`，然后 `launch(backend="patchright")`。
- 优先使用 Playwright，而不是 Puppeteer。
- 使用住宅代理。
- 触发 reCAPTCHA 前在页面停留 15 秒以上。
- 同一会话中的 reCAPTCHA 调用间隔 30 秒以上。
- 使用固定指纹种子。
- 表单输入尽量用 `page.type()`，不要直接 `page.fill()`。
- 减少 reCAPTCHA 检测前的 `page.evaluate()` 调用。

---

## FAQ

### 这合法吗？

CloakBrowser 是基于开源 Chromium 构建的浏览器。项目声明不支持非法用途。未经授权自动化系统、撞库、账号批量注册滥用等行为被明确禁止。完整条款见 `BINARY-LICENSE.md`。

### 和 Camoufox 有什么区别？

Camoufox 修改 Firefox；CloakBrowser 修改 Chromium。Chromium 拥有原生 Playwright 支持、更大的生态，以及更接近真实 Chrome 的 TLS 指纹。

### 检测网站以后会不会识别它？

可能会。机器人检测是攻防对抗。源码级补丁比配置级补丁更难检测，但并非不可能。项目会随检测策略变化进行更新。

### 可以用自己的代理吗？

可以：

```python
launch(proxy="http://user:pass@host:port")
launch(proxy="socks5://user:pass@host:port")
```

HTTP 和 SOCKS5 都支持。

---

## Roadmap

| 功能 | 状态 |
|---|---|
| Linux x64 — Chromium 146，57 patches | 已发布 |
| macOS arm64/x64 — Chromium 145，26 patches | 已发布 |
| Windows x64 — Chromium 146，57 patches | 已发布 |
| JavaScript / Puppeteer / Playwright 支持 | 已发布 |
| 每会话指纹轮换 | 已发布 |
| 内置代理轮换 | 计划中 |

---

## 链接

- Changelog：[`CHANGELOG.md`](CHANGELOG.md)
- 网站：<https://cloakbrowser.dev>
- Issues：<https://github.com/CloakHQ/CloakBrowser/issues>
- PyPI：<https://pypi.org/project/cloakbrowser/>
- npm：<https://www.npmjs.com/package/cloakbrowser>
- Ko-fi：<https://ko-fi.com/cloakhq>
- 邮箱：cloakhq@pm.me

---

## 安全与签名验证

所有 release 都带有供应链验证签名。示例：

```bash
# 验证 GPG 签名
gpg --keyserver keyserver.ubuntu.com --recv-keys C60C0DDC9D0DE2DD
git verify-tag chromium-v146.0.7680.177.3

# 验证 GitHub binary attestation
gh attestation verify cloakbrowser-linux-x64.tar.gz --repo CloakHQ/cloakbrowser

# 验证 Docker 镜像签名
cosign verify \
  --certificate-identity-regexp "https://github.com/CloakHQ/CloakBrowser/" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  cloakhq/cloakbrowser:latest
```

---

## 许可证

- Wrapper 代码：MIT，见 [`LICENSE`](LICENSE)。
- CloakBrowser 二进制文件，即编译后的 Chromium：免费使用，但不可再分发，见 [`BINARY-LICENSE.md`](BINARY-LICENSE.md)。

---

## 贡献者

README 中列出的贡献者包括：

- @evelaa123：humanize 行为、持久化上下文、Windows 修复。
- @yahooguntu：持久化上下文。
- @kitiho：null viewport 修复。
- @eofreternal：humanConfig 类型修复、humanized 方法选项类型。
- @manaskarra：iframe humanized action 作用域修复、GeoIP timeout guard。
- @Youhai020616：SOCKS5 credential encoding logging。
- @AlexTech314：AWS Lambda 集成。
