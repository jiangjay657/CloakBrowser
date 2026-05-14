import os
import sys
from datetime import datetime

class SkillLogger:
    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), "logs")
        
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"outlook_register_{timestamp}.log")
        
        self._write_header()
    
    def _write_header(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write(f"  Outlook 注册日志\n")
            f.write(f"  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
    
    def log(self, level, step, message, details=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] [{level}] [Step {step}] {message}"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
            if details:
                if isinstance(details, str):
                    f.write("  " + details.replace("\n", "\n  ") + "\n")
                else:
                    import json
                    try:
                        f.write("  " + json.dumps(details, ensure_ascii=False, indent=2) + "\n")
                    except:
                        f.write("  " + str(details) + "\n")
            f.write("\n")
        
        print(log_line)
    
    def info(self, step, message, details=None):
        self.log("INFO", step, message, details)
    
    def success(self, step, message, details=None):
        self.log("SUCCESS", step, message, details)
    
    def warning(self, step, message, details=None):
        self.log("WARNING", step, message, details)
    
    def error(self, step, message, details=None):
        self.log("ERROR", step, message, details)
    
    def debug(self, step, message, details=None):
        self.log("DEBUG", step, message, details)
    
    def take_snapshot(self, step, description):
        self.info(step, f"📸 拍摄快照: {description}")
    
    def fill_element(self, step, element_type, value):
        self.info(step, f"✏️  填写 {element_type}: {value}")
    
    def click_element(self, step, element_description):
        self.info(step, f"👆 点击: {element_description}")
    
    def wait_for(self, step, wait_text):
        self.info(step, f"⏳ 等待文本出现: {wait_text}")
    
    def register_result(self, email, password, name, birthday, country, success=True):
        self.log("RESULT" if success else "FAILURE", "Final", 
                 "注册结果汇总", {
                     "邮箱": email,
                     "密码": password,
                     "姓名": name,
                     "生日": birthday,
                     "国家": country
                 })
    
    def finish(self):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"  结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
        print(f"\n📝 日志已保存到: {self.log_file}")


def get_logger():
    return SkillLogger()


if __name__ == "__main__":
    logger = get_logger()
    logger.info("0", "测试日志记录")
    logger.success("0", "测试成功")
    logger.warning("0", "测试警告")
    logger.error("0", "测试错误")
    logger.finish()
