import os
import shutil
import time
from cloakbrowser import launch_persistent_context

os.environ["CLOAKBROWSER_BINARY_PATH"] = r"F:\cloakbrowser-windows-x64\chrome.exe"

USER_DATA_DIR = r"F:\cloak-user-data-1"

if os.path.exists(USER_DATA_DIR):
    shutil.rmtree(USER_DATA_DIR)
os.makedirs(USER_DATA_DIR)

context = launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    headless=False,
    proxy="socks5://14af6435d63a6:b2fc8dbccb@185.101.105.249:12324",
    timezone="America/Denver",
    locale="en-US",
    humanize=True,
    human_preset="careful",
    args=[
        "--no-first-run",
        "--no-default-browser-check",
        "--fingerprint-webrtc-ip=185.101.105.249",
        "--fingerprint-platform=windows",
    ],
)

page = context.new_page()
page.goto("https://outlook.live.com/mail/", timeout=60000)

print("Outlook 已打开，页面标题:", page.title())
print("当前 URL:", page.url)
print("浏览器将保持打开，按 Enter 关闭...")
input()

context.close()
print("浏览器已关闭。")
