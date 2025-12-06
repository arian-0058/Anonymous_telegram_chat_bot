# 🤖 Anonymous Telegram Chat Bot

ربات تلگرامی برای چت ناشناس بین کاربران، با پشتیبانی چندزبانه، پروفایل کاربر و ذخیره‌سازی اطلاعات روی دیتابیس.

---

## ✨ ویژگی‌ها (Features)

- 👥 **چت ناشناس دوطرفه** بین کاربران بدون نمایش آیدی یا نام واقعی  
- 🔍 **جستجوی هم‌صحبت** با دستور `/search`  
- 🔁 **رفتن به نفر بعدی** با دستور `/next`  
- 🛑 **توقف جست‌وجو یا گفت‌وگو** با دستور `/stop`  
- 👤 **پروفایل کاربر** (جنسیت، سن، توضیحات کوتاه و...) با دستور `/profile`  
- 🔗 **ارسال لینک پروفایل** برای هم‌صحبت با دستور `/link`  
- 🌐 **چندزبانه (فارسی / انگلیسی)** با دستور `/language`  
- 🧠 **ذخیره‌سازی در دیتابیس PostgreSQL** (کاربر، وضعیت، گفتگو و...)  
- 🚦 **Throttling / Rate limiting** برای جلوگیری از اسپم و فشار روی بات  
- 🧩 معماری تمیز بر پایه‌ی لایه‌های:
  - `handlers`، `services`، `repositories`، `unit of work`
  - `middlewares` برای مدیریت زبان، کاربر و دیتابیس

---

## 🛠 تکنولوژی‌ها (Tech Stack)

- **Python 3.11+**
- [Aiogram 3.x](https://github.com/aiogram/aiogram) – فریم‌ورک بات تلگرام
- [PostgreSQL](https://www.postgresql.org/) – دیتابیس
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) – ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) – مایگریشن دیتابیس
- [Project Fluent](https://projectfluent.org/) + `aiogram-i18n` – سیستم چندزبانه
- **Docker** و `docker-compose`
- **Poetry** برای مدیریت پکیج‌ها
- ابزارهای توسعه:
  - `mypy`، `ruff`، `Makefile`

---

## 📦 پیش‌نیازها (System dependencies)

- Python 3.11+
- Docker
- docker-compose
- make
- poetry

---

## ⚙️ راه‌اندازی سریع با Docker

### 1. کلون‌کردن ریپو

```bash
git clone https://github.com/arian-0058/anonymous-telegram-chat-bot.git
cd anonymous-telegram-chat-bot
```

### 2. تنظیم متغیرهای محیطی

یک فایل `.env` بر اساس نمونه‌ی موجود بساز:

```bash
cp .env.dist .env
```

سپس داخل `.env` مقادیر رو ویرایش کن:

```env
# توکن ربات تلگرام (از BotFather بگیر)
BOT_TOKEN=123456789:ABCDEF_your_token_here

# تنظیمات PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PASSWORD=pg_password
POSTGRES_USER=postgres
POSTGRES_DB=db_name
POSTGRES_PORT=5432
POSTGRES_DATA=/var/lib/postgresql/data
```

> برای توسعه‌ی لوکال بدون Docker می‌تونی `POSTGRES_HOST=localhost` بزاری.

### 3. اجرای سرویس‌ها با Docker

```bash
docker-compose build
docker-compose up -d --remove-orphans
```

### 4. اجرای مایگریشن‌ها

بعد از بالا آمدن دیتابیس، مایگریشن‌ها رو اجرا کن:

```bash
make migrate
```

یا مستقیم:

```bash
poetry run alembic upgrade head
```

ربات به صورت پیش‌فرض با **polling** اجرا می‌شه و بعد از بالا آمدن کانتینر `bot` آماده‌ی استفاده است.

---

## ⚙️ راه‌اندازی بدون Docker (Development mode)

۱. نصب وابستگی‌ها:

```bash
poetry install
```

۲. تنظیم `.env` مثل بالا (با `POSTGRES_HOST=localhost` و دیتابیس لوکال خودت).  

۳. اجرای مایگریشن:

```bash
poetry run alembic upgrade head
```

۴. اجرای ربات:

```bash
poetry run python -m bot
```

---

## 📁 ساختار پروژه (Project structure)

```text
bot/
  core/           # ساخت و راه‌اندازی bot/dispatcher و runtime
  enums/          # enumهای مربوط به وضعیت کاربر، پروفایل، زبان و...
  handlers/       # هندلرهای دستورات / پیام‌ها (start, profile, search, chatting, ...)
  keyboards/      # کیبوردهای inline و reply
  middlewares/    # middlewareهای i18n، دیتابیس، کاربر و throttling
  repositories/   # لایه‌ی دسترسی به دیتابیس
  services/       # منطق تجاری (business logic)
  utils/          # توابع کمکی مثل logging، جستجوی هم‌صحبت و...

locales/
  en/messages.ftl # متن‌های انگلیسی
  fa/messages.ftl # متن‌های فارسی

migrations/       # اسکریپت‌های Alembic
Dockerfile
docker-compose.yml
pyproject.toml
Makefile
.env.dist
```

---

## 🧪 توسعه و دیباگ

برخی دستورات مفید:

```bash
# پاک کردن کش‌ها و __pycache__
make clean

# چک‌کردن کد (mypy + ruff)
make lint

# ساخت ایمیج‌ها
make app-build

# اجرای سرویس‌ها
make app-run    # docker-compose stop + up -d --remove-orphans
make app-stop   # توقف سرویس‌ها
make app-down   # توقف و حذف کانتینرها
```

---

## 🚀 ایده‌های توسعه‌ی بعدی

- اضافه‌کردن فیلتر براساس جنسیت / سن در جست‌وجوی هم‌صحبت  
- اضافه‌کردن پنل ادمین برای بلاک‌کردن کاربران متخلف  
- اضافه‌کردن متریک‌ها و لاگ‌های پیشرفته (Prometheus / Grafana)  
- اضافه‌کردن تست‌های واحد و integration

---

> اگر این پروژه برات مفید بود، خوشحال می‌شم ⭐️ بدی.
