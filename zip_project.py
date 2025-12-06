import os
import zipfile

EXCLUDE_DIRS = {
    ".venv", "venv", ".git", "__pycache__", ".mypy_cache",
    ".pytest_cache", "node_modules", ".idea", ".vscode"
}
EXCLUDE_FILES = {".DS_Store"}

def zip_project(root_dir, output_filename="atb.zip"):
    """
    فشرده‌سازی پروژه به‌صورت امن (حذف پوشه‌های غیر ضروری و نادیده گرفتن فایل‌های غیرقابل‌دسترسی)
    """
    zip_path = os.path.join(root_dir, output_filename)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            # حذف پوشه‌های غیرضروری از پیمایش
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file == output_filename or file in EXCLUDE_FILES:
                    continue

                full_path = os.path.join(root, file)
                # پرهیز از symlink ها (در ویندوز مشکل‌ساز می‌شوند)
                if os.path.islink(full_path):
                    continue

                rel_path = os.path.relpath(full_path, root_dir)
                try:
                    zipf.write(full_path, rel_path)
                except (OSError, PermissionError) as e:
                    # فایل‌های غیرقابل‌دسترسی را رد کن
                    print(f"⚠️ رد شد: {rel_path} ({e})")

    print(f"✅ فایل ZIP ساخته شد: {zip_path}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"📦 در حال فشرده‌سازی پوشه: {current_dir}")
    zip_project(current_dir)
