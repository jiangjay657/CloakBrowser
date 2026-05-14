import os
import sys
import subprocess
import time
import atexit
from datetime import datetime

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"browser_start_{timestamp}.log")
    
    class Logger:
        def __init__(self, log_file):
            self.log_file = log_file
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("="*80 + "\n")
                f.write(f"  CloakBrowser 启动日志\n")
                f.write(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
        
        def log(self, message):
            timestamp = datetime.now().strftime("%H:%M:%S")
            line = f"[{timestamp}] {message}"
            print(line)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    
    return Logger(log_file)

def main():
    logger = setup_logging()
    logger.log("🚀 正在启动 CloakBrowser...")
    
    # 检查 CloakBrowser 二进制路径
    cloak_binary = os.environ.get("CLOAKBROWSER_BINARY_PATH", r"F:\cloakbrowser-windows-x64\chrome.exe")
    logger.log(f"📦 CloakBrowser 路径: {cloak_binary}")
    
    if not os.path.exists(cloak_binary):
        logger.log(f"❌ 找不到 CloakBrowser 二进制文件: {cloak_binary}")
        logger.log("请设置 CLOAKBROWSER_BINARY_PATH 环境变量指向正确的 chrome.exe 路径")
        return 1
    
    # 用户数据目录
    user_data_dir = os.environ.get("CLOAKBROWSER_USER_DATA_DIR", r"F:\cloak-user-data-1")
    logger.log(f"📁 用户数据目录: {user_data_dir}")
    
    # 清理旧的用户数据（可选，根据需要注释掉）
    if os.path.exists(user_data_dir):
        import shutil
        logger.log("🗑️  清理旧的用户数据目录...")
        shutil.rmtree(user_data_dir)
    os.makedirs(user_data_dir, exist_ok=True)
    
    # 启动参数
    args = [
        cloak_binary,
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--remote-debugging-port=9222",
        "--fingerprint-platform=windows",
        "https://outlook.live.com/mail/?prompt=create_account"
    ]
    
    # 代理设置（可选）
    proxy = os.environ.get("CLOAKBROWSER_PROXY")
    if proxy:
        logger.log(f"🔌 使用代理: {proxy}")
        args.insert(1, f"--proxy-server={proxy}")
    
    # 时区设置（可选）
    timezone = os.environ.get("CLOAKBROWSER_TIMEZONE")
    if timezone:
        logger.log(f"🌐 时区: {timezone}")
        args.insert(1, f"--timezone-for-testing={timezone}")
    
    logger.log(f"📋 启动参数: {' '.join(args)}")
    
    # 启动浏览器
    logger.log("⏳ 正在启动浏览器...")
    process = subprocess.Popen(args)
    
    # 注册退出时清理
    def cleanup():
        if process.poll() is None:
            logger.log("🛑 正在关闭浏览器...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except:
                process.kill()
    
    atexit.register(cleanup)
    
    # 等待浏览器启动
    logger.log("⏱️  等待浏览器启动 (3秒)...")
    time.sleep(3)
    
    logger.log("✅ CloakBrowser 已启动！")
    logger.log("🔗 远程调试端口: 9222")
    logger.log("📧 已自动打开 Outlook 注册页面")
    logger.log("\n💡 浏览器将保持运行，按 Ctrl+C 退出")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        logger.log("\n👋 再见！")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
