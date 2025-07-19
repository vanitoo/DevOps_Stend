import os

# 📂 Укажи папку, где лежат твои .md инструкции
folder = r"C:\Project\vBulletin_convert_Markdown"  # 👈 замени на свою папку

# 🔧 Настройки фронт-маттера
layout = "default"

# Проходим по всем файлам в папке
for filename in os.listdir(folder):
    if filename.lower().endswith(".md"):
        filepath = os.path.join(folder, filename)

        # Читаем старое содержимое
        with open(filepath, "r", encoding="utf-8") as f:
            old_content = f.read()

        # Проверяем, есть ли уже фронт-маттер (чтобы не добавлять повторно)
        if old_content.strip().startswith("---"):
            print(f"[SKIP] Уже есть фронт-маттер: {filename}")
            continue

        # Название для заголовка (без .md)
        title = os.path.splitext(filename)[0]

        # Создаём фронт-маттер
        front_matter = f"---\nlayout: {layout}\ntitle: {title}\n---\n\n"

        # Записываем новый файл
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(front_matter + old_content)

        print(f"[OK] Добавлен фронт-маттер: {filename}")

print("✅ Готово! Все файлы обработаны.")
