import calendar
import base64
import ctypes
import hashlib
import json
import os
import random
import shutil
import socket
import struct
import string
import tempfile
import time
import urllib.parse
import urllib.request
from cloakbrowser import launch_persistent_context

USER_DATA_DIR = tempfile.mkdtemp(
    prefix="cloak-user-data-",
    dir=os.path.join(os.path.expanduser("~"), "Downloads"),
)

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def generate_outlook_email_prefix():
    first_names = [
        "james", "john", "robert", "michael", "david", "william", "richard", "joseph",
        "thomas", "charles", "mary", "patricia", "jennifer", "linda", "barbara",
        "elizabeth", "susan", "jessica", "sarah", "karen", "daniel", "matthew",
        "andrew", "christopher", "joshua", "ryan", "nathan", "brandon", "emma",
        "olivia", "ava", "mia", "sophia", "amelia", "harper", "evelyn", "abigail",
        "emily", "ella", "grace", "chloe", "lily", "hannah", "zoe", "stella",
    ]
    last_names = [
        "smith", "johnson", "williams", "brown", "jones", "garcia", "miller",
        "davis", "rodriguez", "martinez", "anderson", "taylor", "thomas", "moore",
        "jackson", "martin", "lee", "thompson", "white", "harris", "clark", "lewis",
        "walker", "hall", "allen", "young", "king", "wright", "scott", "green",
        "baker", "adams", "nelson", "hill", "campbell", "mitchell", "roberts",
    ]
    first = random.choice(first_names)
    last = random.choice(last_names)
    patterns = [
        lambda: f"{first}{last}",
        lambda: f"{first}.{last}",
        lambda: f"{first}_{last}",
        lambda: f"{first}{last}{random.randint(1, 9999)}",
        lambda: f"{first}.{last}{random.randint(1, 999)}",
        lambda: f"{first[0]}{last}",
        lambda: f"{first[0]}{last}{random.randint(1, 999)}",
        lambda: f"{first}{last[:4]}",
        lambda: f"{first}{random.randint(10, 99)}",
        lambda: f"{first}_{random.randint(1, 9999)}",
    ]
    email_prefix = random.choice(patterns)() + f"{random.randint(1000, 9999)}"
    first_name = first.capitalize()
    last_name = last.capitalize()
    return email_prefix, first_name, last_name


def generate_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*"
    length = random.randint(12, 20)
    required = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    all_chars = uppercase + lowercase + digits + symbols
    remaining = [random.choice(all_chars) for _ in range(length - len(required))]
    chars = required + remaining
    random.shuffle(chars)
    return "".join(chars)


class CdpWebSocket:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.sock = None
        self.next_id = 0

    def __enter__(self):
        parsed = urllib.parse.urlparse(self.ws_url)
        host = parsed.hostname
        port = parsed.port or 80
        path = parsed.path
        if parsed.query:
            path += f"?{parsed.query}"

        self.sock = socket.create_connection((host, port), timeout=5)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self.sock.sendall(request.encode("ascii"))
        response = self._read_http_response()
        accept = base64.b64encode(
            hashlib.sha1(
                (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")
            ).digest()
        ).decode("ascii")
        if " 101 " not in response or accept not in response:
            raise RuntimeError("CDP WebSocket 握手失败")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.sock is not None:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def send(self, method, params=None):
        self.next_id += 1
        message_id = self.next_id
        self._send_text(
            json.dumps(
                {
                    "id": message_id,
                    "method": method,
                    "params": params or {},
                },
                separators=(",", ":"),
            )
        )
        while True:
            message = json.loads(self._recv_text())
            if message.get("id") != message_id:
                continue
            if "error" in message:
                raise RuntimeError(message["error"])
            return message.get("result", {})

    def _read_http_response(self):
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            data += chunk
        return data.decode("iso-8859-1", errors="replace")

    def _read_exact(self, size):
        data = b""
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise RuntimeError("CDP WebSocket 连接已关闭")
            data += chunk
        return data

    def _send_text(self, text):
        payload = text.encode("utf-8")
        header = bytearray([0x81])
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))

        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def _recv_text(self):
        while True:
            first, second = self._read_exact(2)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(8))[0]
            mask = self._read_exact(4) if masked else b""
            payload = self._read_exact(length)
            if masked:
                payload = bytes(
                    byte ^ mask[index % 4] for index, byte in enumerate(payload)
                )

            if opcode == 1:
                return payload.decode("utf-8")
            if opcode == 8:
                raise RuntimeError("CDP WebSocket 已关闭")
            if opcode == 9:
                self._send_pong(payload)

    def _send_pong(self, payload):
        header = bytearray([0x8A, 0x80 | len(payload)])
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)


def get_attrs(node):
    attrs = node.get("attributes", [])
    return dict(zip(attrs[0::2], attrs[1::2]))


def iter_cdp_nodes(node):
    yield node
    for key in ("children", "shadowRoots", "pseudoElements"):
        for child in node.get(key, []) or []:
            yield from iter_cdp_nodes(child)
    if node.get("contentDocument"):
        yield from iter_cdp_nodes(node["contentDocument"])


def quad_to_box(quad):
    xs = quad[0::2]
    ys = quad[1::2]
    left = min(xs)
    top = min(ys)
    right = max(xs)
    bottom = max(ys)
    return {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "width": right - left,
        "height": bottom - top,
        "center_x": (left + right) / 2,
        "center_y": (top + bottom) / 2,
    }


def get_hsprotect_challenge_ws_url(timeout=60000):
    deadline = time.monotonic() + timeout / 1000
    while time.monotonic() < deadline:
        with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=3) as res:
            targets = json.loads(res.read().decode("utf-8"))
        for target in targets:
            url = target.get("url", "")
            if (
                target.get("type") == "iframe"
                and "iframe.hsprotect.net/index.html" in url
                and "ch_ctx=1" in url
                and target.get("webSocketDebuggerUrl")
            ):
                return target["webSocketDebuggerUrl"]
        time.sleep(0.25)
    raise RuntimeError("未找到 hsprotect 可见挑战 iframe 的 CDP target")


def get_press_and_hold_box_from_cdp(ws_url, timeout=60000):
    deadline = time.monotonic() + timeout / 1000
    with CdpWebSocket(ws_url) as cdp:
        cdp.send("DOM.enable")
        while time.monotonic() < deadline:
            document = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
            for node in iter_cdp_nodes(document["root"]):
                if node.get("nodeName") != "P":
                    continue
                html = cdp.send("DOM.getOuterHTML", {"nodeId": node["nodeId"]}).get(
                    "outerHTML",
                    "",
                )
                if ">Press and hold</p>" not in html:
                    continue
                try:
                    model = cdp.send("DOM.getBoxModel", {"nodeId": node["nodeId"]})[
                        "model"
                    ]
                except Exception:
                    continue
                box = quad_to_box(model["border"])
                if box["width"] > 0 and box["height"] > 0:
                    return box
            time.sleep(0.25)
    raise RuntimeError("未找到 iframe 内 Press and hold 的可见 p 标签")


def move_system_mouse_to_press_and_hold_label(page, timeout=60000):
    page.wait_for_function(
        r"""() => {
            const frame = Array.from(document.querySelectorAll("iframe"))
                .find((el) => el.title === "Verification challenge"
                    && el.src.includes("iframe.hsprotect.net")
                    && el.src.includes("ch_ctx=1"));
            if (!frame) return false;
            const rect = frame.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0;
        }""",
        timeout=timeout,
    )
    page_info = page.evaluate(
        r"""() => {
            const frame = Array.from(document.querySelectorAll("iframe"))
                .find((el) => el.title === "Verification challenge"
                    && el.src.includes("iframe.hsprotect.net")
                    && el.src.includes("ch_ctx=1"));
            const rect = frame.getBoundingClientRect();
            const chromeLeft = (window.outerWidth - window.innerWidth) / 2;
            const chromeTop = window.outerHeight - window.innerHeight - chromeLeft;
            return {
                frame: {
                    left: rect.left,
                    top: rect.top,
                    width: rect.width,
                    height: rect.height,
                },
                chromeLeft,
                chromeTop,
                screenX: window.screenX,
                screenY: window.screenY,
            };
        }"""
    )
    label_box = get_press_and_hold_box_from_cdp(
        get_hsprotect_challenge_ws_url(timeout=timeout),
        timeout=timeout,
    )
    viewport_x = page_info["frame"]["left"] + label_box["center_x"]
    viewport_y = page_info["frame"]["top"] + label_box["center_y"]
    screen_x = page_info["screenX"] + page_info["chromeLeft"] + viewport_x
    screen_y = page_info["screenY"] + page_info["chromeTop"] + viewport_y

    ctypes.windll.user32.SetCursorPos(round(screen_x), round(screen_y))
    return {
        "viewport_x": viewport_x,
        "viewport_y": viewport_y,
        "screen_x": screen_x,
        "screen_y": screen_y,
        "frame": page_info["frame"],
        "label_box": label_box,
    }


def mouse_left_click(hold_seconds=0.08):
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(hold_seconds)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def perform_press_and_hold(mouse_target, hold_seconds=15):
    start_x = round(mouse_target["screen_x"])
    start_y = round(mouse_target["screen_y"])
    move_right = random.randint(0, 20)
    hold_x = start_x + move_right

    mouse_left_click()
    time.sleep(0.2)
    ctypes.windll.user32.SetCursorPos(hold_x, start_y)
    time.sleep(0.1)

    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    try:
        time.sleep(hold_seconds)
    finally:
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    return {
        "move_right": move_right,
        "hold_x": hold_x,
        "hold_y": start_y,
        "hold_seconds": hold_seconds,
    }


context = None

try:
    context = launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        proxy="socks5://14af6435d63a6:b2fc8dbccb@185.101.105.249:12324",
        # geoip=True,
        timezone="America/Denver",
        locale="en-US",
        humanize=True,
        human_preset="careful",
        args=[
            "--no-first-run",
            "--no-default-browser-check",
            "--remote-debugging-port=9222",
            "--fingerprint-webrtc-ip=185.101.105.249",
            "--fingerprint-platform=windows",
        ],
    )

    page = context.new_page()
    page.goto("https://www.microsoft.com/en-us/microsoft-365/outlook/log-in", timeout=60000)

    print("Microsoft 已打开，当前 URL:", page.url)
    print("页面标题:", page.title())

    create_account = page.locator(
        'main a[href*="2125440"]:visible',
        has_text="Create a free account",
    ).first
    with context.expect_page(timeout=60000) as new_page_info:
        create_account.click(timeout=30000)
    signup_page = new_page_info.value
    signup_page.wait_for_load_state("domcontentloaded", timeout=60000)

    print("点击创建免费账号，当前 URL:", signup_page.url)
    print("页面标题:", signup_page.title())

    email_prefix, first_name, last_name = generate_outlook_email_prefix()
    full_email = f"{email_prefix}@outlook.com"

    signup_page.get_by_label("New email").fill(email_prefix, timeout=30000)
    signup_page.get_by_role("button", name="Next").click(timeout=30000)
    signup_page.get_by_role("heading", name="Create your password").wait_for(timeout=60000)

    print("已输入随机邮箱:", full_email)
    print("点击 Next 后页面标题:", signup_page.title())

    password = generate_password()
    signup_page.locator('input[type="password"][autocomplete="new-password"]').fill(
        password,
        timeout=30000,
    )
    signup_page.get_by_role("button", name="Next").click(timeout=30000)
    signup_page.get_by_role("heading", name="Add some details").wait_for(timeout=60000)

    print("已输入随机密码:", password)
    print("点击密码页 Next 后页面标题:", signup_page.title())

    birth_year = random.randint(1980, 2003)
    birth_month = random.randint(1, 12)
    birth_month_name = calendar.month_name[birth_month]
    birth_day = random.randint(1, calendar.monthrange(birth_year, birth_month)[1])

    signup_page.locator("#BirthMonthDropdown").click(force=True, timeout=30000)
    signup_page.get_by_role("option", name=birth_month_name, exact=True).click(
        timeout=30000,
    )
    signup_page.locator("#BirthDayDropdown").click(force=True, timeout=30000)
    signup_page.get_by_role("option", name=str(birth_day), exact=True).click(
        timeout=30000,
    )
    signup_page.get_by_label("Birth year").fill(str(birth_year), timeout=30000)
    signup_page.get_by_role("button", name="Next").click(timeout=30000)
    signup_page.get_by_role("heading", name="Add your name").wait_for(timeout=60000)

    print("已输入随机生日:", f"{birth_month_name} {birth_day}, {birth_year}")
    print("点击生日页 Next 后页面标题:", signup_page.title())

    signup_page.locator("#firstNameInput").fill(first_name, timeout=30000)
    signup_page.locator("#lastNameInput").fill(last_name, timeout=30000)
    signup_page.get_by_role("button", name="Next").click(timeout=30000)
    signup_page.wait_for_timeout(5000)

    print("已输入姓名:", first_name, last_name)
    print("点击姓名页 Next 后页面标题:", signup_page.title())

    mouse_target = move_system_mouse_to_press_and_hold_label(signup_page)
    print(
        "已移动电脑鼠标到 iframe 内 Press and hold 中心:",
        f"viewport=({mouse_target['viewport_x']:.1f}, {mouse_target['viewport_y']:.1f})",
        f"screen=({mouse_target['screen_x']:.1f}, {mouse_target['screen_y']:.1f})",
    )
    hold_result = perform_press_and_hold(mouse_target)
    print(
        "已执行 Press and hold 操作:",
        f"右移={hold_result['move_right']}px",
        f"长按坐标=({hold_result['hold_x']}, {hold_result['hold_y']})",
        f"时长={hold_result['hold_seconds']}s",
    )

    print("浏览器将保持打开，按 Enter 关闭...")
    input()
except Exception as exc:
    print(f"执行出错：{exc}")
    raise
finally:
    if context is not None:
        context.close()
        print("浏览器已关闭。")
    shutil.rmtree(USER_DATA_DIR, ignore_errors=True)
