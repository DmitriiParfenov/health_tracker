# health_tracker

Health_tracker — это SPA-приложение для отслеживания и улучшения своего ежедневного поведения путем создания привычек,
которые пользователь хочет выработать. Возможно установить периодичность и точное время отправки уведомлений для прививания
привычек в свою повседневную жизнь. При наступлении времени выполнения привычки, трекер узнает у пользователя, выполнил ли
текущий пользователь задание или нет. В случае успешного выполнения трекер отправит одобрительное сообщение или направит 
последнего на выполнение приятной привычки, в противном случае — отправит мотивированное сообщение.

Сайт написан на Python с использованием Django для запросов пользователя. Для обмена данными между приложениями по сети используется Django REST-Framework, 
интеграция с Telegram для отправки уведомлений — через API Telegram-сервисы. Для создания периодических задач — celery-beat, 
а для отложенных — celery. База данных — PostgreSQL, брокер — redis.

# Дополнительная информация

- Для создания суперпользователя из директории `health_tracker` выполните в консоли: </br>
```
python manage.py csu
```
- Для просмотра покрытия кода тестами введите в консоли:
```
coverage run --source='.' manage.py test
coverage report
```
- Для получения качественного анализа программного кода введите в консоли:
```
flake8 --config .flake8
```

- Для запуска отложенных задач выполните в консоли из директории `health_tracker`: </br>
```
celery -A config worker -l info
```

- Для запуска периодических задач выполните в консоли из директории `health_tracker`: </br>
```
celery -A config worker -l info
celery -A config beat -l info -S django
```

# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/health_tracker.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/health_tracker.git
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```
# Установка и настройка Redis

- Установите Redis, если он не установлен. Для этого выполните в консоли:
```
sudo apt install redis-server
``` 
- Запустите Redis, выполнив в консоли:
```
sudo service redis-server start
``` 
- Произойдет запуск Redis сервера на порту 6379. Для того, чтобы убедиться, что сервер запущен, необходимо выполнить
в консоли команду, ответом которой должен быть `PONG`.
```
redis-cli ping
```

# Работа с базой данной PostgreSQL

- Установите PostgreSQL, если он не установлен. Для этого, например для Ubuntu, выполните в консоли:
```
sudo apt install postgresql
```
- Выполните вход в интерактивную оболочку PostgreSQL от имени `postgresql`, выполнив в консоли:
```
sudo -i -u postgres psql
```
- Создайте базу данный для проекта, выполнив в консоли:
```
CREATE DATABASE health_tracker;
```
- Закройте интерактивную оболочку PostgreSQL:
```
\q
```
# Работа с переменными окружения

- В директории `health_tracker` создайте файл `.env`. Пример содержимого файла:
- Пример содержимого файла `.env` для запуска сервиса через docker:
```
HOST=название текущего хоста — db (из docker-compose)
NAME=название базы данных — postgres
USER=имя текущего пользователя — postgres
PASSWORD=пароль текущего пользователя — ваш пароль

POSTGRES_USER=имя пользователя — postgres
POSTGRES_PASSWORD=пароль пользователя — ваш пароль 
POSTGRES_DB=название базы данных для подключения из docker — db (из docker-compose)

EMAIL_BACKEND=путь импорта Python для вашего класса бэкенда
EMAIL_HOST=хост SMTP
EMAIL_HOST_USER=адрес электронной почты для аутентификации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутентификации на почтовом сервере

TELEGRAM_API_KEY=API ключ для подключения платежей

LOCATION=местоположение используемого кеша (redis://redis:6379)
``` 
- Пример содержимого файла `.env` для запуска сервиса на локальной машине без docker:
```
HOST=название текущего хоста — localhost
NAME=название базы данных — health_tracker
USER=имя текущего пользователя — postgres
PASSWORD=пароль текущего пользователя — ваш пароль

POSTGRES_USER=имя пользователя — postgres
POSTGRES_PASSWORD=пароль пользователя — ваш пароль 
POSTGRES_DB=название базы данных для подключения из docker — db (из docker-compose)

EMAIL_BACKEND=путь импорта Python для вашего класса бэкенда
EMAIL_HOST=хост SMTP
EMAIL_HOST_USER=адрес электронной почты для аутентификации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутентификации на почтовом сервере

STRIPE_API_KEY=API ключ для подключения платежей

TELEGRAM_API_KEY=местоположение используемого кеша (redis://127.0.0.1:6379)
``` 
# Получение токена для доступа к HTTP API Telegram

- Создайте свой телеграм-бот с помощью бота [BotFather](https://t.me/botfather) через команду `/newbot`.
- Следуйте инструкциям бота.
- Сохраните ключ API от `BotFather` в папке `env` в переменную окружения `TELEGRAM_API_KEY`.
- Перейдите по ссылке, полученной от `BotFather`, для старта бота.

# Работа с миграциями

Из директории `health_tracker` выполните в консоли: </br>

```
python manage.py migrate
```

# Запуск сервера Django

- Активируйте виртуальное окружение согласно п. `Клонирование репозитория` </br>

- Из директории `health_tracker` выполните в консоли: </br>
```
python3 manage.py runserver
```
- Запустите отложенные задачи, выполнив в консоли: </br>
```
celery -A config worker -l info
```

- Запустите периодические задачи, выполнив в консоли: </br>
```
celery -A config beat -l info -S django
```

# Запуск сервера Django c использованием docker-compose

- Установите `docker` согласно инструкции на сайте [docker](https://www.docker.com/get-started/). </br>
- Запустите образ для запуска нескольких контейнеров с использованием `docker-compose`. Для этого из директории `health_tracker` выполните в консоли: </br>
```
docker-compose build
```
- Запустите собранный образ. Для этого из директории `health_tracker` выполните в консоли: </br>
```
docker-compose up
```
- Или для запуска образа в фоновом режим из директории `health_tracker` выполните в консоли: </br>
```
docker-compose up -d
```
- В новой открытой сессии создайте суперпользователя. Для этого из директории `health_tracker` выполните в консоли: </br>
```
docker-compose exec web python manage.py csu
```
- Сервис будет доступен по URL `http://127.0.0.1:8000/` </br>
- Для остановки работы образа из директории `health_tracker` в консоли нажмите `CTRL + C`: </br>
- Для удаления остановленного образа из директории `health_tracker` в консоли выполните: </br>
```
docker-compose down
```
