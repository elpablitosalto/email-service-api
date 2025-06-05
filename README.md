# Email Service API

## Структура проекта

```
email-service-api/
│
├── app/
│   ├── api/           # Эндпоинты FastAPI
│   ├── models/        # Pydantic-схемы и SQLAlchemy-модели
│   ├── services/      # Логика работы с почтой и БД
│   ├── repository/    # Работа с БД
│   ├── core/          # Настройки, логирование
│   └── main.py        # Точка входа FastAPI
│
├── tests/             # Тесты pytest
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Микросервис для отправки и получения электронной почты с REST API на FastAPI.

## Запуск

```bash
git clone <repo_url>
cd email-service-api
docker compose up --build -d
```

- API будет доступен на http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- MailHog Web UI: http://localhost:8025

## Деплой на VPS с доменом и nginx

1. **Откройте порт 8000 на сервере (если используете другой порт — откройте его):**
   ```bash
   sudo ufw allow 8000/tcp
   ```

2. **Настройте nginx для проксирования запросов на FastAPI:**
   Создайте файл `/etc/nginx/sites-available/email-service-api` со следующим содержимым:
   ```nginx
   server {
       listen 80;
       server_name your-domain;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   Затем выполните:
   ```bash
   sudo ln -s /etc/nginx/sites-available/email-service-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. **Запустите сервисы:**
   ```bash
   docker compose up --build -d
   ```

4. **Проверьте доступность:**
   Перейдите по адресу: http://your-domain

5. **(Рекомендуется) Настройте HTTPS через Let's Encrypt:**
   [Инструкция по Let's Encrypt](https://letsencrypt.org/)

---

Если возникнут проблемы — проверьте логи nginx и контейнера FastAPI.

## Переменные окружения

См. файл `.env` для настройки подключения к БД и почтовому серверу.

## Тесты

```bash
docker compose exec api pytest
```

## Эндпоинты
- `POST /emails/send` — отправка письма
- `GET /emails` — список писем с фильтрацией
- `GET /emails/stats` — статистика по письмам 