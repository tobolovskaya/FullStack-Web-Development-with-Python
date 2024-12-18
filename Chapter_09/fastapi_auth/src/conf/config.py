class Config:
    DB_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/todo_app"
    JWT_SECRET = "your_secret_key"  # Секретний ключ для токенів
    JWT_ALGORITHM = "HS256"  # Алгоритм шифрування токенів
    JWT_EXPIRATION_SECONDS = 3600  # Час дії токена (1 година)


config = Config
