\# Star Agents Marketplace

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

## 📋 Опис проекту

**Star Agents Marketplace** - це сучасний веб-додаток для маркетплейсу AI-агентів, побудований на FastAPI. Проект надає платформу для:

- 🔐 **Аутентифікації користувачів** через JWT-токени
- 👥 **Управління користувачами та агентами** з повним CRUD функціоналом
- 💳 **Системи покупок** агентів з історією транзакцій
- 📊 **RESTful API** з автоматичною документацією
- ✅ **Комплексного тестування** з pytest
- 🎨 **Веб-інтерфейсу** для взаємодії з API

Проект демонструє best practices сучасної веб-розробки з використанням FastAPI, SQLAlchemy та сучасних підходів до тестування.

## 🛠 Використані технології

### Backend
- **FastAPI** - високопродуктивний веб-фреймворк для Python
- **SQLAlchemy** - ORM для роботи з базами даних
- **Alembic** - система міграцій баз даних
- **Pydantic** - валідація даних та серіалізація
- **Python-JOSE** - робота з JWT токенами
- **Passlib** - хешування паролів

### Тестування
- **pytest** - фреймворк для unit та integration тестів
- **httpx** - асинхронний HTTP клієнт для тестів
- **pytest-asyncio** - підтримка асинхронних тестів

### Інструменти розробки
- **Uvicorn** - ASGI сервер для FastAPI
- **SQLite** - вбудована база даних (можна замінити на PostgreSQL/MySQL)

### Фронтенд
- **HTML5/CSS3** - статичні сторінки
- **JavaScript** - клієнтська логіка
- **Jinja2** - шаблонізатор

## 📁 Структура проекту

```
ai_agent_project/
├── app/                          # Основний додаток
│   ├── __init__.py
│   ├── main.py                   # Точка входу FastAPI
│   ├── database.py               # Конфігурація БД
│   ├── models.py                 # SQLAlchemy моделі
│   ├── schemas.py                # Pydantic схеми
│   ├── crud.py                   # CRUD операції
│   ├── auth_utils.py             # Утиліти аутентифікації
│   ├── utils.py                  # Загальні утиліти
│   └── routers/                  # API роутери
│       ├── __init__.py
│       ├── auth.py               # Аутентифікація
│       ├── users.py              # Користувачі
│       ├── agents.py             # Агенти
│       └── purchases.py          # Покупки
├── tests/                        # Тести
│   ├── __init__.py
│   ├── conftest.py               # Фікстури pytest
│   ├── test_auth.py              # Тести аутентифікації
│   └── test_purchases.py         # Тести покупок
├── static/                       # Статичні файли
│   ├── index.html
│   ├── login.html
│   ├── agents.html
│   └── purchases.html
├── templates/                    # Jinja2 шаблони
│   ├── index.html
│   └── marketplace.html
├── alembic/                      # Міграції БД
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── __pycache__/                  # Python кеш (ігнорується)
├── alembic.ini                   # Конфігурація Alembic
├── pytest.ini                    # Конфігурація pytest
├── requirements.txt              # Python залежності
├── package.json                  # Node.js залежності (якщо потрібно)
├── server.js                     # Node.js сервер (опціонально)
├── myagent.code-workspace        # VS Code workspace
├── check_db.py                   # Скрипт перевірки БД
├── client.py                     # HTTP клієнт для тестування
└── README.md                     # Цей файл
```

## 💻 Вимоги до системи

- **Python** 3.8+
- **pip** (входить до Python)
- **Git** (для клонування репозиторію)
- **Веб-браузер** (для доступу до інтерфейсу)

## 🚀 Інсталяція та запуск

### 1. Клонування репозиторію

```bash
git clone https://github.com/yourusername/ai_agent_project.git
cd ai_agent_project
```

### 2. Створення віртуального середовища

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Інсталяція залежностей

```bash
pip install -r requirements.txt
```

### 4. Запуск додатку

#### Режим розробки (з автоперезавантаженням)
```bash
uvicorn app.main:app --reload
```

#### Production режим
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Додаток буде доступний за адресою: http://localhost:8000

## ⚙️ Конфігурація

### Змінні середовища (.env)

Створіть файл `.env` в кореневій директорії проекту:

```env
# База даних
DATABASE_URL=sqlite:///./star_agents.db

# JWT конфігурація
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Налаштування сервера
HOST=0.0.0.0
PORT=8000

# Режим розробки
DEBUG=True
```

### Конфігурація бази даних

За замовчуванням використовується SQLite. Для production рекомендується PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/star_agents
```

## 📚 API Документація

FastAPI автоматично генерує інтерактивну документацію API:

### Swagger UI
- **URL**: http://localhost:8000/docs
- **Опис**: Повна інтерактивна документація з можливістю тестування API
- **Особливості**:
  - Інтерактивні форми для відправки запитів
  - Автоматична валідація параметрів
  - Відображення прикладів відповідей
  - Авторизація через JWT токени

### ReDoc
- **URL**: http://localhost:8000/redoc
- **Опис**: Альтернативна документація в стилі OpenAPI
- **Особливості**:
  - Читаємий дизайн
  - Детальна специфікація
  - Експорт в різні формати

## 🔗 Приклади API ендпоінтів

### Аутентифікація

#### Реєстрація користувача
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "is_active": true
  }'
```

#### Логін (отримання JWT токена)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"
```

**Відповідь:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Робота з агентами

#### Створення агента
```bash
curl -X POST "http://localhost:8000/agents/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Analyzer Agent",
    "role": "data_analyst"
  }'
```

#### Отримання списку агентів
```bash
curl -X GET "http://localhost:8000/agents/"
```

### Покупки (вимагають авторизації)

#### Створення покупки
```bash
curl -X POST "http://localhost:8000/purchases/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 1,
    "agent_id": 1
  }'
```

#### Отримання власних покупок
```bash
curl -X GET "http://localhost:8000/purchases/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Відповідь:**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "timestamp": "2024-01-15T10:30:00Z",
    "agent_name": "Data Analyzer Agent",
    "agent_role": "data_analyst"
  }
]
```

## 🧪 Тестування

Проект включає комплексну систему тестування з використанням pytest.

### Запуск всіх тестів
```bash
pytest
```

### Запуск з детальним виводом
```bash
pytest -v
```

### Запуск конкретного тестового файлу
```bash
pytest tests/test_auth.py
pytest tests/test_purchases.py
```

### Запуск з покриттям коду
```bash
pytest --cov=app --cov-report=html
```

### Структура тестів

- **test_auth.py**: Тести аутентифікації
  - Успішний логін
  - Невдалий логін (неправильний пароль)
  - Невдалий логін (неіснуючий користувач)

- **test_purchases.py**: Тести системи покупок
  - Доступ без авторизації (401)
  - Порожній список покупок для нового користувача
  - Створення покупки
  - Перегляд покупок після створення

### Фікстури тестування

- `client`: TestClient з перевизначеною БД
- `db_session`: Тестова сесія БД (SQLite in-memory)
- `test_user`: Створює тестового користувача

## 🗺 Roadmap

## 📋 To Do — Release 1.1.0

### ✅ Testing
- [ ] Додати тести для CRUD операцій агентів
- [ ] Перевірити edge cases (некоректні дані, відсутні агенти)

### 🎨 UI/UX
- [ ] Замінити `alert()` на Bootstrap alerts
- [ ] Винести навбар у Jinja2 шаблон
- [ ] Додати базові стилі для мобільної адаптивності

### ⚙️ Configuration
- [ ] Перехід на PostgreSQL для production
- [ ] Реалізувати валідацію email при реєстрації

### 🛠 DevOps
- [ ] Створити Dockerfile та docker-compose для локального запуску
- [ ] Налаштувати CI/CD pipeline (GitHub Actions або GitLab CI)
- [ ] Автоматичні тести та деплой на staging

### 🚀 Functionality
- [ ] Додати рейтинги та відгуки для агентів
- [ ] Реалізувати пагінацію списку агентів
- [ ] Впровадити кешування для популярних запитів (Redis)
- [ ] Інтеграція з платіжними системами (Stripe/PayPal)
- [ ] WebSocket для оновлень у реальному часі

### ✅ Версія 1.0.0 (Поточна)
- [x] Базова аутентифікація через JWT
- [x] CRUD операції для користувачів та агентів
- [x] Система покупок
- [x] Unit та integration тести
- [x] Веб-інтерфейс
- [x] Автоматична API документація

### 🔄 Плановані покращення

#### Версія 1.1.0
- [ ] Інтеграція з зовнішніми AI сервісами
- [ ] Система рейтингів та відгуків
- [ ] Пагінація для великих списків
- [ ] Кешування відповідей (Redis)
- [ ] Логування дій користувачів

#### Версія 1.2.0
- [ ] WebSocket підтримка для real-time оновлень
- [ ] Система повідомлень
- [ ] Інтеграція з платіжними системами
- [ ] Адмін панель
- [ ] API rate limiting

#### Версія 2.0.0
- [ ] Міграція на PostgreSQL
- [ ] Docker контейнеризація
- [ ] CI/CD pipeline
- [ ] GraphQL API
- [ ] Mobile додаток

### 🐛 Відомі проблеми
- SQLite використовується замість PostgreSQL для production
- Відсутня валідація email адрес
- Обмежена обробка помилок

## 📄 Ліцензія

Цей проект розповсюджується під ліцензією MIT. Дивіться файл `LICENSE` для деталей.

## 📞 Контакти

- **Автор**: [Ваше ім'я]
- **Email**: your.email@example.com
- **GitHub**: [https://github.com/yourusername](https://github.com/yourusername)
- **LinkedIn**: [Ваш профіль](https://linkedin.com/in/yourprofile)

## 🤝 Внесок у проект

1. Fork проект
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit зміни (`git commit -m 'Add some AmazingFeature'`)
4. Push до branch (`git push origin feature/AmazingFeature`)
5. Відкрийте Pull Request

Будь ласка, переконайтеся що:
- Ваш код проходить всі тести
- Додано відповідну документацію
- Код відповідає PEP 8 стандартам

---

⭐ Якщо проект вам сподобався, поставте зірочку на GitHub!



