from cloakbrowser import launch


# 有头模式：显示浏览器窗口
browser = launch(headless=False)

# 使用 HTTP 或 SOCKS5 代理
browser = launch(proxy="socks5://14af6435d63a6:b2fc8dbccb@185.101.105.249:12324",
                timezone="America/New_York", 
                locale="en-US",
                humanize=True, 
                human_preset="careful", 
                args=["--fingerprint-webrtc-ip=auto"])


