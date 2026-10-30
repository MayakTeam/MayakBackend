# MayakBackend
Это репозиторий с кодом сервера для MayakDefect.


## Стек технологий
- FastAPI
- SQL Alchemy
- Pydantic
- Elasticsearch

## Техдолг
- Валидация паролей методами pydantic
- Подключение к БД по пути, указанным в config.py

## ERD

```mermaid
erDiagram
    ROLES ||--o{ USERS : "назначена"
    USERS ||--o{ REPORTS : "автор"
    USERS ||--o{ COMMENTS : "пишет"
    USERS ||--o{ CONFIRMATIONS : "подтверждает"
    USERS ||--o{ ATTACHMENTS : "загружает"
    USERS }o--o| WORKSHOPS : "цех по умолчанию"

    STATUSES ||--o{ REPORTS : "имеет"
    REPORTS ||--o{ COMMENTS : "содержит"
    REPORTS ||--o{ CONFIRMATIONS : "подтверждается"
    REPORTS |o--o{ ATTACHMENTS : "вложение"
    COMMENTS |o--o{ ATTACHMENTS : "вложение"
    CONFIRMATIONS |o--o{ ATTACHMENTS : "вложение"
    WORKSHOPS ||--o{ CONFIRMATIONS : "целевой цех"

    ROLES {
        int id PK
        string name UK
        json permissions
    }

    USERS {
        int id PK
        string username UK
        string password_hash
        int role_id FK
        int default_workshop_id FK "nullable"
        datetime created_at
        datetime last_login_at "nullable"
    }

    STATUSES {
        int id PK
        string name UK
    }

    WORKSHOPS {
        int id PK
        string name UK
    }

    REPORTS {
        int id PK
        string title
        string description
        int author_id FK
        int status_id FK
        datetime created_at
        datetime last_updated_at
    }

    COMMENTS {
        int id PK
        int report_id FK
        int author_id FK
        string text
        datetime created_at
    }

    CONFIRMATIONS {
        int id PK
        int report_id FK
        int user_id FK
        int workshop_id FK
        string text
        datetime confirmed_at
    }

    ATTACHMENTS {
        int id PK
        int report_id FK "nullable"
        int comment_id FK "nullable"
        int confirmation_id FK "nullable"
        string url
        int user_id FK
        datetime created_at
    }
```