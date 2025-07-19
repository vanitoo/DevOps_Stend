import os

from datetime import datetime
import requests
import strip
from bs4 import BeautifulSoup
import html2text
import re
import urllib3
from urllib.parse import urljoin, urlparse
from hashlib import md5

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VBulletinImageDownloader:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': base_url
        }
        self.processed_messages = set()  # Для отслеживания уже обработанных сообщений

    def normalize_url(self, img_url):
        """Преобразует URL в абсолютный и исправляет пути vBulletin"""
        if not img_url:
            return None

        if img_url.startswith(('http://', 'https://')):
            return img_url

        if img_url.startswith(('./', 'filedata/', 'core/')):
            base = urlparse(self.base_url)
            return f"{base.scheme}://{base.netloc}/{img_url.lstrip('./')}"

        return urljoin(self.base_url, img_url)

    def download_image(self, img_url, folder="images"):
        img_url = self.normalize_url(img_url)
        if not img_url:
            return None

        try:
            os.makedirs(folder, exist_ok=True)

            parsed = urlparse(img_url)
            filename = parsed.path.split('/')[-1] or f"image_{hash(img_url)}.jpg"

            if 'filedata/fetch' in img_url:
                params = dict(p.split('=') for p in parsed.query.split('&'))
                filename = f"img_{params.get('id', '0')}_{params.get('d', '0')}.jpg"

            filepath = os.path.join(folder, filename)

            print(f"\n🔍 Загружаем: {img_url}")
            print(f"📁 Сохраняем как: {filepath}")

            response = self.session.get(img_url, stream=True, verify=False, timeout=15)
            response.raise_for_status()

            if not response.headers.get('Content-Type', '').startswith('image/'):
                print(f"❌ Не изображение (Content-Type: {response.headers.get('Content-Type')})")
                return None

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print("✅ Успешно сохранено")
            return filepath

        except Exception as e:
            print(f"❌ Ошибка: {str(e)}")
            return None


def convert_vbulletin_to_markdown(url):
    print("🚀 Начало обработки темы...")

    downloader = VBulletinImageDownloader(url)

    try:
        print(f"\n🌐 Загружаем страницу: {url}")
        response = downloader.session.get(url, verify=False, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Ошибка загрузки страницы: {str(e)}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Untitled"
    print(f"\n📌 Тема: {title}")

    # Создаем безопасное имя файла
    safe_title = re.sub(r'[^\w\-_\. ]', '_', title)[:100]  # Ограничиваем длину и заменяем спецсимволы
    # output_file = f"{safe_title}.md"

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"{current_time}_{safe_title}.md"



    # Точный поиск по классу сообщения
    posts = soup.find_all('div', class_=re.compile(r'b-post__content js-post__content'))

    if not posts:
        posts = soup.find_all('div', class_='b-post__content')

    print(f"\n📊 Найдено сообщений: {len(posts)}")

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0

    markdown_content = f"# {title}\n\n"
    image_counter = 0

    for i, post in enumerate(posts, 1):
        author_tag = post.find_previous('a', class_=re.compile(r'username|author'))
        author = author_tag.get_text(strip=True) if author_tag else "Anonymous"

        date_tag = post.find_previous('span', class_=re.compile(r'date|time'))
        date = date_tag.get_text(strip=True) if date_tag else "Unknown date"

        print(f"\n📝 Сообщение {i}/{len(posts)} от {author} ({date})")

        for img in post.find_all('img'):
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue

            local_path = downloader.download_image(img_url)
            if local_path:
                image_counter += 1
                img['src'] = local_path
                print(f"🖼️ [Изображение {image_counter}] Сохранено: {local_path}")

        post_md = h.handle(str(post))
        markdown_content += f"## {author} ({date})\n\n{post_md}\n\n---\n\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n🎉 Готово!")
    print(f"📄 Тема сохранена в файл: {output_file}")
    print(f"📊 Всего сообщений: {len(posts)}")
    print(f"🖼️ Сохранено изображений: {image_counter}")
    print(f"📁 Папка с изображениями: {os.path.abspath('../images')}")


if __name__ == "__main__":
    url = input("Введите URL темы vBulletin: ").strip()
    convert_vbulletin_to_markdown(url)
