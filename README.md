# echo bot ps

---
* aiogram  
* Docker  
* PostgreSQL  
* Redis  
---
### Структура бота

```markdown
📁 db_echo_bot - корневая директория всего проекта;  
📁 app - основная директория приложения;  
📁 bot - директория с модулями и пакетами, относящимися непосредственно к боту;  
📁 enums - директория, в которой хранятся модули с перечислениями (Enum'ы);  
- roles.py - модуль с перечислениями, относящимися к ролям пользователей;  
📁 filters - директория с самописными фильтрами;  
- filters.py - модуль с фильтрами, которые мы напишем под конкретные задачи бота;  
📁 handlers - пакет с обработчиками;  
- admin.py - модуль с обработчиками апдейтов от пользователей с ролью UserRole.ADMIN;  
- others.py - модуль с обработчиком (эхо-хэндлером) апдейтов, которые не попали в другие хэндлеры;  
- settings.py - модуль с обработчиками апдейтов, связанных с настройками языка пользователя;  
- user.py - модуль с хэндлерами пользователей;  
📁 i18n - пакет с объектами, отвечающими за интернационализацию бота;  
- translator.py - модуль с функцией, которая готовит переводы для бота;  
📁 keyboards - пакет с клавиатурами бота;  
- keyboards.py - модуль с инлайн-клавиатурами;  
- menu_button.py - модуль для настроек кнопки Menu;  
📁 middlewares - пакет с миддлварями;  
- database.py - модуль с миддлварью для получения соединения из пула соединений, открытия транзакции и 
    прокидывания соединения по цепочке обработки апдейта;  
- i18n.py - модуль с миддлварью для выбора словаря с переводами, в зависимости от языка пользователя;  
- lang_settings.py - модуль со вспомогательной миддлварью, обеспечивающей отображение текстов на 
    выбранном пользователем языке, в процессе настроек языка;  
- shadow_ban.py - миддлварь для игнорирования апдейтов от забаненных пользователей;  
- statistics.py - миддлварь для подсчёта активности пользователей;  
📁 states - пакет для хранения модулей с группами состояний (FSM);  
- states.py - модуль для хранения групп состояний пользователей;  
- __init__.py - вспомогательный модуль - инициализатор пакета;  
- bot.py - модуль с функцией конфигурации бота;  
📁 infrastructure - директория для сопутствующей инфраструктуры приложения;  
📁 database - директория c объектами для работы с реляционной БД;  
- connection.py - модуль с функциями для создания одиночного подключения и пула подключений к реляционной БД;  
- db.py - модуль с функциями, через которые будут осуществляться запросы к БД;  
📁 config - директория с модулем конфигурации приложения;  
- config.py - модуль для конфигурации приложения;  
📁 locales - директория с переводами;  
📁 en - директория для контента на английском языке;  
- txt.py - модуль с текстами на английском языке;  
📁 ru - директория для контента на русском языке;  
- txt.py - модуль с текстами на русском языке;  
📁 migrations - директория для миграций БД;
- create_tables.py - модуль с кодом создания таблиц в БД;
```

---



# Telegram Echo Bot with PostgreSQL, Redis, and Admin Tools

This project is a **Telegram Echo Bot** powered by `aiogram`, designed to demonstrate practical integration with a **relational database (PostgreSQL)** and **Redis**. The bot includes **user role management**, **language selection**, and **admin tools** for moderation and user analytics.

## Features

### Core Functionality

- **Echo replies**: Replies to all user messages.
- **User registration**: Automatically stores new users in the `users` table.
- **Activity tracking**: Tracks user interactions per day in the `statistics` table.
- **Multilingual interface**: Allows users to set interface language (EN / RU).
- **Role-based behavior**: Distinguishes between regular users and admins.

### Admin Features

- `/ban <@username|user_id>`: Ban a user.
- `/unban <@username|user_id>`: Unban a user.
- `/statistics`: View top active users.

## Tech Stack

- **Python 3.13** — Primary language of the project.
- **aiogram** – Fast and flexible Telegram bot framework for Python.
- **PostgreSQL** – Relational DB to persist users and their activity.
- **Redis** – FSM storage for aiogram.
- **pgAdmin** – Visual database management for PostgreSQL.
- **Docker** — Used to run infrastructure services like PostgreSQL, Redis, and pgAdmin.

## Running the Bot

> This project uses **Docker Compose** to run PostgreSQL, Redis, and pgAdmin.

1. Clone the repository:

```bash
git clone https://github.com/kmsint/aiogram3_stepik_course.git
```
2. Move to the db_echo_bot folder:

```bash
cd aiogram3_stepik_course/db_echo_bot
```

3. Create **.env** file and copy the code from **.env.example** file into it.

4. Fill in the file **.env** with real data (`BOT_TOKEN`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.)

5. Launch containers with Postgres, Redis, and pgAdmin with the command (You need docker and docker-compose installed on your local machine):

```bash
docker compose up -d
```

6. Create a virtual environment in the project root and activate it.

7. Install the required libraries in the virtual environment with `pip`:

```bash
pip install -r requirements.txt
```
```commandline
uv add -r requirements.txt
```

8. Apply database migrations using the command:

```bash
python3 -m migrations.create_tables
```

7. Run main.py to launch the bot:

```bash
python3 main.py
```

## Bot Behavior

### Command `/start`:

- Adds user to users table if not existing.
- Records initial language.
- Assigns user or admin role.
- Logs activity in statistics.
- Displays localized `/help` message and `Menu`.

### Command `/help`:

- Shows user-friendly command summary (localized).
- Logs activity to statistics.

### Command `/lang`:

- Lets user choose interface language (EN/RU).
- Updates DB and button labels accordingly.

### Commands `/ban` and `/unban` (admin only):

- Bans/unbans by @username or user_id.
- Handles input validation.

## Notes

- User status is updated to `is_alive=false` if the bot is blocked.
- All roles and bans are DB-driven; no hardcoded access.

## Feedback

Have ideas or issues? Open a GitHub Issue or contact the maintainer.

## License

This project is licensed under the **MIT License**.

