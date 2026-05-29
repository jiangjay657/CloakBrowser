import calendar
import random
import shutil
import string
import tempfile
from cloakbrowser import launch_persistent_context

USER_DATA_DIR = tempfile.mkdtemp(
    prefix="cloak-user-data-",
    dir=r"C:\Users\jiangj\Downloads",
)

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
    return random.choice(patterns)()


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


def derive_names_from_email_prefix(email_prefix):
    separators = [".", "_", "-"]
    for separator in separators:
        parts = [part for part in email_prefix.split(separator) if part]
        if len(parts) >= 2:
            return parts[0].capitalize(), parts[1].capitalize()

    letters = "".join(char for char in email_prefix if char.isalpha())
    if len(letters) >= 6:
        split_at = max(3, len(letters) // 2)
        return letters[:split_at].capitalize(), letters[split_at:].capitalize()

    return "James", "Smith"


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

    email_prefix = generate_outlook_email_prefix()
    full_email = f"{email_prefix}@outlook.com"
    first_name, last_name = derive_names_from_email_prefix(email_prefix)

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
