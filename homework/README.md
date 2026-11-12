# Гостевая книга на Flask

Учебный проект по теме «Python и Web». Добавьте отзыв через HTML-форму или JSON API, отфильтруйте список по имени автора и проверьте, что отзывы сохранились после перезапуска приложения. Оба интерфейса работают с одной базой SQLite.

## Как запустить

Установите Python 3.10 или новее. Скачайте или клонируйте репозиторий и откройте терминал в папке с файлом `app.py`.

**macOS и Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app init-db
python app.py
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe app.py
```

Откройте [гостевую книгу](http://127.0.0.1:5000/tasks). Чтобы остановить сервер, нажмите `Ctrl+C` в терминале. При следующем запуске на macOS и Linux сначала активируйте окружение. Затем выполните последнюю команду для своей системы.

Команда `init-db` создаёт таблицу в `instance/guestbook.sqlite3`. Эту команду можно повторить, и существующие задачи сохранятся.

## Первые запросы

Добавьте отзыв на странице и откройте список в JSON. Найдите поля id, author, review и created.
Введите имя автора в поле фильтра и нажмите «Найти». Откройте фильтр отзывов в JSON и проверьте, что в ответ попали только отзывы этого автора.
Вернитесь на страницу отзывов. Нажмите правой кнопкой по странице и выберите «Просмотреть код» или «Исследовать». На вкладке **Network** («Сеть») включите **Preserve log** и добавьте ещё один отзыв. В **Payload** запроса POST /reviews найдите поля author и text. В **Headers** проверьте статус 303 и заголовок Location: /reviews. Следующий запрос GET /reviews загрузит обновлённый список.

## JSON API

| Запрос | Что делает | Успешный ответ |
| --- | --- | --- |
| `GET /api/recall` | Возвращает все отзывы. Параметр `author` оставляет отзывы только указанного автора. |	`200 OK`, объект с массивом `reviews` |
| `POST /api/recall` | Создаёт отзыв из JSON `{"author": "Аня", "review": "Отличный сайт!"}`. | `201 Created`, объект новой задачи |

Для POST укажите `Content-Type: application/json`. Имя автора должно содержать от 1 до 80 символов, а текст отзыва — от 1 до 2000 символов после удаления пробелов по краям. При неверном фильтре, теле запроса или названии сервер вернёт `400 Bad Request`. Если заголовок `Content-Type` отсутствует или указывает тип данных, отличный от JSON, сервер вернёт `415 Unsupported Media Type`.

В другом терминале запустите клиент на HTTPX. На macOS и Linux активируйте окружение командой `source .venv/bin/activate`. В PowerShell используйте `.\.venv\Scripts\python.exe` вместо `python`.

```bash
python client.py
python client.py --add "Петр" "устал пока делал"
python client.py --author "Петр"
```

В requests.http есть готовые запросы для HTTP-клиента IDE, в том числе запросы с ошибками. Попробуйте отправить пустое имя или текст и сравнить ответ с ответом на корректный запрос.

## Где смотреть код

| Файл | Что в нём |
| --- | --- |
| [app.py](app.py) | Маршруты Flask, проверка ввода и обработка запросов |
| [db.py](db.py) и [schema.sql](schema.sql) | Подключение к SQLite и создание таблицы recall |
| [templates/tasks.html](templates/review.html) | Шаблон страницы, форма добавления и список отзывов |
| [client.py](client.py) | Отправка запросов через HTTPX и чтение ответа |
| [tests/test_app.py](tests/test_app.py) | Тесты pytest для HTTP-ответов и сохранения данных |
