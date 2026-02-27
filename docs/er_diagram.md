```mermaid
erDiagram

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role "user/admin"
        datetime created_at
    }

    ORDER {
        int id PK
        int user_id FK
        string title
        text description
        string status "new/accepted/done"
        datetime created_at
    }
```
