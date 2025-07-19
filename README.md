# 🚀 DevOps Stend

Добро пожаловать в **DevOps Stend** — здесь собраны мои инструкции и пошаговые гайды по настройке инфраструктуры, сервисов и DevOps‑инструментов.

Сайт автоматически публикуется на **GitHub Pages** и доступен по адресу:  
👉 [https://vanitoo.github.io/DevOps_Stend/](https://vanitoo.github.io/DevOps_Stend/)

---

## 📋 Содержание

- [Главная страница](https://vanitoo.github.io/DevOps_Stend/index.html)
- [Roadmap в виде блоков](https://vanitoo.github.io/DevOps_Stend/roadmap.html)
- Отдельные инструкции:
  - [01. Блок схема](https://vanitoo.github.io/DevOps_Stend/01_блок_схема.html)
  - [02. Установка proxmox](https://vanitoo.github.io/DevOps_Stend/02_установка_proxmox.html)
  - [03. Настройка шлюза (Ubuntu 20.04)](https://vanitoo.github.io/DevOps_Stend/03_Настройка_шлюза_(Ubuntu_20.04).html)
  - [04. Настройка OpenVPN Server](https://vanitoo.github.io/DevOps_Stend/04_Настройка_OpenVPN_Server.html)
  - …и так далее по списку.

Полный список страниц вы можете найти на сайте или в файле [`index.md`](index.md).

---

## 🏗 Структура репозитория

```text
_config.yml             # Конфигурация Jekyll
index.md                # Главная страница
roadmap.md              # Страница со списком в виде блоков
_layouts/
  default.html          # Кастомный шаблон для всех страниц
assets/
  css/style.css         # Стили
<номер>_<название>.md   # Инструкции (каждая отдельная страница)
.github/
  workflows/jekyll-gh-pages.yml  # CI/CD для GitHub Pages
