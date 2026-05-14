---
name: "outlook-register"
description: "自动注册 Outlook 邮箱。使用 Chrome Dev MCP 操控 CloakBrowser 隐身浏览器，全自动填写表单并完成长按人机验证。Invoke when user asks to register/create an Outlook email account automatically."
---

# Outlook 自动注册

全程使用 Chrome Dev MCP 工具自动注册 Outlook 邮箱。

## 📝 日志记录

所有操作都会详细记录到日志文件中，方便问题分析。

### 日志文件位置
```
f:\CloakBrowser\.trae\skills\outlook-register\logs\
```

### 日志文件命名
- 浏览器启动日志: `browser_start_YYYYMMDD_HHMMSS.log`
- 注册流程日志: `outlook_register_YYYYMMDD_HHMMSS.log`

### 日志级别
- `INFO` - 普通信息
- `SUCCESS` - 成功操作
- `WARNING` - 警告信息
- `ERROR` - 错误信息
- `DEBUG` - 调试信息
- `RESULT` - 最终结果

---

## 前置条件

- Chrome Dev MCP 已连接并可用

## 快速开始 - 自动启动浏览器

### 方式一：一键启动（推荐）

在 skill 目录下有一个 `start_cloakbrowser.py` 脚本，可以自动启动 CloakBrowser：

```bash
cd f:\CloakBrowser\.trae\skills\outlook-register
python start_cloakbrowser.py
```

这个脚本会：
- 自动配置 CloakBrowser 启动参数
- 开启远程调试端口 9222
- 自动打开 Outlook 注册页面
- 保持浏览器运行直到手动停止
- 所有操作记录到日志文件


---

## 注册流程

### 🔧 Step 0 — 初始化日志记录

首先，使用 Python 初始化日志记录器：

```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('0', '开始 Outlook 注册流程')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 0.5 — 启动浏览器（自动执行）

**Skill 执行开始时，先检查浏览器是否已启动：**

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('0', '检查浏览器是否已启动')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. 首先列出当前打开的页面：
```
mcp__Chrome_DevTools_MCP_list_pages
```

2. 如果没有可用页面，则自动启动浏览器：
记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('0', '浏览器未启动，正在启动 CloakBrowser')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

启动浏览器：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python start_cloakbrowser.py", blocking: false, requires_approval: false, target_terminal: "new"
```

3. 等待 5 秒让浏览器启动，然后再次列出页面：
```
mcp__Chrome_DevTools_MCP_list_pages
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('0', '浏览器已启动，列出可用页面')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

4. 选择刚打开的页面：
```
mcp__Chrome_DevTools_MCP_select_page → pageId: <找到的页面ID>
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('0', '已选择页面，页面ID: <找到的页面ID>')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 1 — 打开注册页（如果尚未打开）

**重要说明**：注册入口地址 `https://outlook.live.com/mail/?prompt=create_account` 加载时间会比较长，请耐心等待。加载成功后会自动跳转到**个人数据导出许可**页面。

如果浏览器启动时没有自动跳转到注册页，则手动导航：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('1', '导航到 Outlook 注册页面（加载时间可能较长）')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
mcp__Chrome_DevTools_MCP_navigate_page → type: "url", url: "https://outlook.live.com/mail/?prompt=create_account"
```

等待页面加载完成（使用 wait_for 检测许可页关键字）：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.wait_for('1', '等待个人数据导出许可页面加载')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
wait_for → text: ["同意", "Accept", "许可", "Privacy"]
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('1', '许可页面加载完成')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
mcp__Chrome_DevTools_MCP_take_snapshot
```

点击同意个人数据导出许可按钮：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('1', '同意许可按钮')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <同意按钮uid>
```

等待页面跳转到注册页：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.wait_for('1', '等待跳转到注册页')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
wait_for → text: ["Create free account", "Sign up", "创建账号", "注册"]
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('1', '已同意许可，准备进入注册页')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
mcp__Chrome_DevTools_MCP_take_snapshot
```

定位到创建账号的表单区域。如果页面上有 "Create free account" 或 "Sign up" 之类的引导，确认已进入注册页。

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('1', '已进入注册页面')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

## 随机数据生成规则

**开始前，必须先生成所有随机数据并保存在变量中**。使用 `evaluate_script` 在页面 JS 上下文中生成并返回所有数据：

```javascript
function() {
  const firstNames = ['James', 'Michael', 'Robert', 'David', 'John', 'William', 'Richard', 'Thomas', 'Daniel', 'Matthew', 'Christopher', 'Andrew', 'Joseph', 'Joshua', 'Ryan'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Wilson', 'Anderson', 'Taylor', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin'];
  
  const letters = 'abcdefghijklmnopqrstuvwxyz';
  let randomPrefix = '';
  for (let i = 0; i < 6; i++) {
    randomPrefix += letters.charAt(Math.floor(Math.random() * letters.length));
  }
  const randomNum = Math.floor(1000 + Math.random() * 9000);
  const emailPrefix = randomPrefix + randomNum;
  
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
  let password = '';
  for (let i = 0; i < 12; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  
  const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
  const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
  const birthYear = Math.floor(1985 + Math.random() * 18);
  const birthMonth = Math.floor(1 + Math.random() * 12);
  const birthDay = Math.floor(1 + Math.random() * 28);
  const country = 'United States';
  
  return {
    emailPrefix,
    email: emailPrefix + '@outlook.com',
    password,
    firstName,
    lastName,
    fullName: firstName + ' ' + lastName,
    birthYear,
    birthMonth,
    birthDay,
    birthday: birthYear + '-' + String(birthMonth).padStart(2, '0') + '-' + String(birthDay).padStart(2, '0'),
    country
  };
}
```

执行上述代码获取随机数据后，将返回结果保存为变量供后续步骤使用。

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('Data', '生成随机数据', {'邮箱': '<生成的邮箱>', '姓名': '<生成的姓名>', '生日': '<生成的生日>'})\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

## 注册流程

### Step 2 — 填写邮箱地址

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('2', '开始填写邮箱地址')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. 先 `take_snapshot` 获取当前页面元素树
```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('2', '获取邮箱输入页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

2. 找到邮箱/用户名输入框（通常 `type="email"` 或 label 含 "new email" / "username" / "Create account"）
3. 用 `fill` 填入随机生成的邮箱前缀（不需要写 `@outlook.com`，Microsoft 会自动补全）

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.fill_element('2', '邮箱', '<随机生成的邮箱前缀>')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
fill → uid: <输入框uid>, value: "<随机生成的邮箱前缀>"
```

4. 点击 "Next" 按钮

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('2', 'Next 按钮')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <Next按钮uid>
```

5. 用 `wait_for` 等待页面跳转

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.wait_for('2', 'Create a password 或 Password')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
wait_for → text: ["Create a password", "Password", "创建密码"]
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('2', '邮箱地址填写完成')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 3 — 填写密码

页面切换到密码输入页后：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('3', '开始填写密码')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. 先 `take_snapshot`
```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('3', '获取密码输入页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

2. 找到密码输入框
3. `fill` 填入随机生成的密码

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.fill_element('3', '密码', '***********')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
fill → uid: <密码框uid>, value: "<随机生成的密码>"
```

4. 如果有"确认密码"输入框，再填一次
5. 取消勾选 "promotional email" 复选框（如果有）
6. 点击 "Next"

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('3', 'Next 按钮')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <Next按钮uid>
```

7. `wait_for` 等待跳转

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.wait_for('3', '国家 或 出生 或 Birthdate')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
wait_for → text: ["国家", "出生", "Birthdate", "Country"]
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('3', '密码填写完成')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 4 — 填写国家与出生日期

密码提交后进入此页。

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('4', '开始填写国家与出生日期')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. `take_snapshot`
```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('4', '获取出生日期页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

2. **国家/地区**：保持默认值，不需要修改
3. 填写出生日期：
   - **年份**：`spinbutton`（输入框），直接 `fill` 填入

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.fill_element('4', '出生年份', '<随机生成的年份>')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
fill → uid: <年份spinbutton>, value: "<随机生成的年份>"
```

   - **月**：`combobox`（下拉框），先 `click` 聚焦，再用下方向键+回车键选择对应月份

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('4', '月份下拉框')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <月份combobox>
press_key → key: "ArrowDown" (按 <目标月份 - 1> 次)
press_key → key: "Enter"
```

   - **日**：`combobox`（下拉框），先 `click` 聚焦，再用下方向键+回车键选择对应日期

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('4', '日期下拉框')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <日期combobox>
press_key → key: "ArrowDown" (按 <目标日期 - 1> 次)
press_key → key: "Enter"
```

4. 点击 "Next"

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('4', 'Next 按钮')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <Next按钮uid>
```

5. `wait_for` → text: "姓名" 或 "First name"

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.wait_for('4', '姓名 或 姓氏 或 First name')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
wait_for → text: ["姓名", "姓氏", "First name", "Last name"]
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('4', '出生日期填写完成')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 4.5 — 填写姓名

出生日期提交后进入姓名填写页。

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('4.5', '开始填写姓名')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. `take_snapshot`
```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('4.5', '获取姓名填写页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

2. 填写姓和名：
   - **姓氏 (Last Name)**：`textbox`，`fill` 填入随机姓
   - **名字 (First Name)**：`textbox`，`fill` 填入随机名

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.fill_element('4.5', '姓氏', '<随机生成的姓>'); logger.fill_element('4.5', '名字', '<随机生成的名>')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
fill_form → [{uid: <姓氏textbox>, value: "<随机生成的姓>"}, {uid: <名字textbox>, value: "<随机生成的名>"}, {uid: <推广复选框>, value: "false"}]
```

3. **取消勾选**推广邮件复选框（如果有）
4. 勾选服务协议（如果有）
5. 点击 "Next"

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.click_element('4.5', 'Next 按钮')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

```
click → uid: <Next按钮uid>
wait_for → text: 进入人机验证或直接跳转
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.success('4.5', '姓名填写完成')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 5 — 🔑 长按人机验证（核心步骤）

这一步是注册成功与否的关键。Microsoft 会显示一个需要**长按**的按钮，按住不放直到动画/进度条走完。

**重要说明**：人机验证按钮通常嵌套在多层 iframe 中，必须逐层查找才能找到正确的按钮元素。

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('5', '开始长按人机验证')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

**判断是否进入验证页的方法**：
- `take_snapshot` 后发现页面上有类似 "Hold"、"Press and hold" 或大圆形按钮
- 页面没有文字输入框，只有交互性元素

```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('5', '获取验证页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

**执行长按的方法** — 使用 `evaluate_script`，**支持多层 iframe 嵌套查找**：

```javascript
async () => {
  // 递归查找 iframe 中的元素
  async function findButtonInFrames(win, depth = 0) {
    if (depth > 10) return null; // 防止无限递归
    
    const selectors = [
      '[role="button"]',
      'button[type="button"]',
      'div[class*="hold"]',
      'div[class*="press"]',
      'div[class*="verify"]',
      'div[id*="proof"]',
      'div[id*="challenge"]',
      '#proof',
      'iframe'
    ];
    
    // 先在当前窗口查找按钮
    for (const sel of selectors.filter(s => s !== 'iframe')) {
      const btn = win.document.querySelector(sel);
      if (btn) {
        const rect = btn.getBoundingClientRect();
        if (rect.width > 50 && rect.height > 50) {
          return { window: win, element: btn };
        }
      }
    }
    
    // 如果没找到，查找 iframe 并递归
    const iframes = win.document.querySelectorAll('iframe');
    for (const iframe of iframes) {
      try {
        const iframeWin = iframe.contentWindow || iframe.contentDocument?.defaultView;
        if (iframeWin) {
          const result = await findButtonInFrames(iframeWin, depth + 1);
          if (result) return result;
        }
      } catch (e) {
        // 跨域 iframe 会抛错，忽略继续
      }
    }
    
    return null;
  }
  
  // 查找按钮
  const result = await findButtonInFrames(window);
  
  if (!result) {
    // 如果递归没找到，尝试查找页面上最大的可交互元素
    let btn = null;
    const allBtns = [...document.querySelectorAll('button, [role="button"], div[tabindex]')];
    if (allBtns.length > 0) {
      btn = allBtns.sort((a, b) => {
        const aSize = a.getBoundingClientRect().width * a.getBoundingClientRect().height;
        const bSize = b.getBoundingClientRect().width * b.getBoundingClientRect().height;
        return bSize - aSize;
      })[0];
    }
    
    if (!btn) return { error: '未找到长按按钮' };
    result = { window: window, element: btn };
  }
  
  const { window: targetWin, element: btn } = result;
  const rect = btn.getBoundingClientRect();
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  
  // 派发 pointerdown（长按开始）
  btn.dispatchEvent(new PointerEvent('pointerdown', {
    clientX: cx, clientY: cy, bubbles: true, cancelable: true,
    pointerId: 1, pointerType: 'touch', isPrimary: true, pressure: 0.5
  }));
  btn.dispatchEvent(new MouseEvent('mousedown', { clientX: cx, clientY: cy, bubbles: true }));
  
  // 持续按住（最多等 15 秒，每 500ms 检查一次是否已完成）
  const startTime = Date.now();
  const maxHold = 15000;
  let completed = false;
  
  while (Date.now() - startTime < maxHold) {
    await new Promise(r => setTimeout(r, 500));
    // 检查按钮是否消失或页面是否变化（验证通过）
    if (!targetWin.document.body.contains(btn) || btn.offsetParent === null) {
      completed = true;
      break;
    }
    // 检查是否有 success/完成 标识
    const bodyText = targetWin.document.body.innerText.toLowerCase();
    if (bodyText.includes('success') || bodyText.includes('verified') || bodyText.includes('complete') || bodyText.includes('done')) {
      completed = true;
      break;
    }
    // 检查主页面是否跳转
    if (window !== targetWin) {
      try {
        const mainBodyText = document.body.innerText.toLowerCase();
        if (mainBodyText.includes('outlook') || mainBodyText.includes('inbox') || mainBodyText.includes('mail')) {
          completed = true;
          break;
        }
      } catch (e) {}
    }
  }
  
  // 派发 pointerup（长按结束）
  btn.dispatchEvent(new PointerEvent('pointerup', {
    clientX: cx, clientY: cy, bubbles: true, cancelable: true,
    pointerId: 1, pointerType: 'touch', isPrimary: true
  }));
  btn.dispatchEvent(new MouseEvent('mouseup', { clientX: cx, clientY: cy, bubbles: true }));
  
  return { success: true, holdDuration: Date.now() - startTime, completed, foundInIframe: window !== targetWin };
}
```

**执行方式**：
```
mcp__Chrome_DevTools_MCP_evaluate_script → function: 上述JS代码
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('5', '长按验证执行完成', {'holdDuration': 'xxxms', 'completed': true})\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

### Step 6 — 确认注册成功

长按验证通过后，页面会自动跳转：

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.info('6', '检查注册结果')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

1. `take_snapshot` 检查页面状态
```
mcp__Chrome_DevTools_MCP_take_snapshot
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.take_snapshot('6', '获取结果页快照')\"", blocking: true, requires_approval: false, target_terminal: "new"
```

2. 用 `evaluate_script` 检查 URL：

```javascript
() => { return { url: window.location.href, title: document.title }; }
```

3. 如果 URL 包含 `outlook.live.com/mail` 或页面标题包含 "Outlook" / "Inbox"，说明注册成功
4. 打印注册结果给用户：

```
✅ 注册成功！
📧 邮箱:   <随机生成的邮箱>
🔑 密码:   <随机生成的密码>
👤 姓名:   <随机生成的姓名>
🎂 生日:   <随机生成的生日>
📍 国家:   United States
```

记录日志：
```
RunCommand → command: "cd f:\CloakBrowser\.trae\skills\outlook-register ; python -c \"from logger import get_logger; logger = get_logger(); logger.register_result('<随机生成的邮箱>', '<随机生成的密码>', '<随机生成的姓名>', '<随机生成的生日>', 'United States', True); logger.finish()\"", blocking: true, requires_approval: false, target_terminal: "new"
```

---

## 异常处理

| 情况 | 处理方式 | 日志记录 |
|------|---------|---------|
| 注册入口页面加载超时 | 重新导航到注册页面，或检查网络连接 | `logger.error('1', '注册页面加载超时，准备重试')` |
| 邮箱已被占用 | 在原有的随机数上加 1，重新填写 | `logger.warning('2', '邮箱已被占用，尝试新邮箱', {'old': 'xxx', 'new': 'yyy'})` |
| 密码不符合要求 | 检查页面提示，增加特殊字符或长度 | `logger.error('3', '密码不符合要求', {'hint': '页面提示'})` |
| 出现额外验证步骤（手机号等） | `take_snapshot` 截图告知用户，暂停等待指示 | `logger.warning('X', '出现额外验证步骤，需要人工介入')` |
| 长按验证失败 | 如果页面回到许可页，重新走 Step 1；否则重试 Step 5 | `logger.error('5', '长按验证失败，准备重试')` |
| 任何步骤卡住超时 | 重新 `take_snapshot`，分析当前页面状态，重新定位元素 | `logger.error('X', '步骤超时，重新分析页面')` |
| 页面跳转了但结构不同 | 不要假设 DOM 结构，每步都先 `take_snapshot` 再操作 | `logger.warning('X', '页面结构变化，重新分析')` |
| 刷新后回到许可页面 | 重新从 Step 1 开始执行流程 | `logger.warning('1', '页面回到许可页，重新开始流程')` |

---

## 注意事项

- **注册入口页面加载时间较长**，请耐心等待，不要频繁刷新
- **每步操作前必须先 `take_snapshot`**，不要使用缓存的 UID
- **每步操作都要记录日志**，使用 logger 工具
- **所有数据必须随机生成**，不要写死任何值
- 所有输入框用 `fill` 工具，不要用 `type_text`
- 下拉框（月份、日期）使用 `click` + `ArrowDown` + `Enter` 组合操作
- **长按验证必须递归查找 iframe**，Microsoft 的验证按钮通常嵌套在多层 iframe 中
- 长按验证使用 `evaluate_script`，模拟 `pointerdown` + 持续等待 + `pointerup`
- CloakBrowser 已处理反检测，无需额外设置
- 不要使用 Playwright/Puppeteer API，只用 Chrome Dev MCP 工具
- 日志文件保存在 `logs/` 目录，出现问题时先查看日志
