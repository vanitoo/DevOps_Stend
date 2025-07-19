
import os

folder = r"C:\Project\vBulletin_convert_Markdown"
for filename in os.listdir(folder):
    if filename.endswith(".md") and " " in filename:
        new_name = filename.replace(" ", "_")
        os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
        print(f"Переименован: {filename} -> {new_name}")
