import os
import shutil
import tempfile
import time
from pathlib import Path

from cloakbrowser import launch_persistent_context

PROFILE_ROOT = Path.home() / "Downloads"
PROFILE_PREFIX = "cloak-user-data-"

# 本机代理默认使用 SOCKS5；如果你的代理软件只开放 HTTP，把它改成 http://127.0.0.1:7897
PROXY_URL = "http://127.0.0.1:7897"

# 指纹检测页
START_URL = "https://abrahamjuliot.github.io/creepjs/"

# 国家环境交给 geoip 根据代理出口自动匹配。
# 例如：美国代理会尽量匹配美国 timezone/locale，日本代理会尽量匹配日本 timezone/locale。
# 如需强制美国，可改为：LOCALE = "en-US"，TIMEZONE = "America/New_York"
LOCALE = None
TIMEZONE = None


def cleanup_old_profiles() -> None:
    """清理上次运行留下的临时用户环境。"""
    if not PROFILE_ROOT.exists():
        return

    for item in PROFILE_ROOT.iterdir():
        if not item.is_dir() or not item.name.startswith(PROFILE_PREFIX):
            continue

        try:
            shutil.rmtree(item)
            print(f"已清理旧 profile: {item}", flush=True)
        except Exception as exc:
            print(f"清理旧 profile 失败，已跳过: {item} ({exc})", flush=True)


def create_profile_dir() -> str:
    """创建本次运行专用的新用户环境目录。"""
    return tempfile.mkdtemp(prefix=PROFILE_PREFIX, dir=PROFILE_ROOT)


def wait_until_browser_closed(context) -> None:
    """保持脚本运行，直到用户关闭所有浏览器窗口。"""
    print("浏览器已启动，可像正常浏览器一样使用。关闭所有浏览器窗口或按 Ctrl+C 退出脚本。", flush=True)

    while True:
        try:
            if not context.pages:
                break
            time.sleep(1)
        except KeyboardInterrupt:
            print("收到 Ctrl+C，准备关闭浏览器...", flush=True)
            break
        except Exception:
            # context 被浏览器关闭后，访问 pages 可能抛异常，此时直接退出等待。
            break


def main() -> None:
    cleanup_old_profiles()

    user_data_dir = create_profile_dir()

    print(f"本次 profile: {user_data_dir}", flush=True)
    print("本次 fingerprint seed: 由 CloakBrowser 自动随机生成", flush=True)
    print(f"代理: {PROXY_URL}", flush=True)
    print(f"启动页: {START_URL}", flush=True)

    context = launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        proxy=PROXY_URL,
        geoip=True,
        locale=LOCALE,
        timezone=TIMEZONE,
        humanize=True,
        human_preset="careful",
        args=[
            "--no-first-run",
            "--no-default-browser-check",
            "--fingerprint-platform=windows",
        ],
    )

    try:
        page = context.new_page()
        page.goto(START_URL, timeout=600000)
        wait_until_browser_closed(context)
    finally:
        try:
            context.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
