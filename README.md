# Mini app

Этот проект представляет собой Telegram-бота с интеграцией Web App, созданного с использованием библиотеки [aiogram](https://docs.aiogram.dev/).

## Версия

``bash 
Version: 0.1.0.dev0
``
## Описание

Бот отвечает на команду `/start` и отправляет кнопку для открытия Web App внутри Telegram. Web App позволяет пользователю взаимодействовать с кастомной веб-страницей, а данные из Web App отправляются обратно боту.

## Функциональность

- Реакция на команду `/start`
- Отправка клавиатуры с кнопкой для открытия Web App
- Построен на базе aiogram 3.x
- Использует ngrok(https://ngrok.com) для локального HTTPS-туннелирования во время разработки

## Требования

- Python 3.7 или выше
- Установленные библиотеки:
  - `aiogram`
  - `aiohttp`
  - `python-dotenv`
- ngrok для локальной разработки

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/your_username/telegram-bot-project.git
   ```
2. **Создание виртуального окружения**
    ```bash
    python -m venv name_of your_venv
    ```
    ```bash
    source .path_to_yours_directory/bin/activate
    ```
2. **Утановите зависимости**
    ```bash
    pip install -r /path/to/requirements.txt
    ```
3. **Скачайте ngrok и распакуйте его в /bin**
    ```bash
    sudo unzip ~/Downloads/ngrok-v3-stable-darwin.zip -d /usr/local/bin
    ```
4. **Установите токен**
    ```bash
    ngrok config add-authtoken your_token
    ```
5. **Деплой**
    ```bash
    ngrok http http://localhost:8080
    ```
6. **Создание бота**
* Получите токен от *BotFather* и web_url ииз ngrok
* Создайте файл `.env` в корневой директории проекта и добавьте следующие строки:
    ```dotenv
    API_TOKEN= your_token
    WEBAPP_URL=https://your_ngrok_url.ngrok.io

    ```
## Запуск
1. **В рабочей дирректории напишите**
    ```bash
    python main.py
    ```