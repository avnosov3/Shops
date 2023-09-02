from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_ENGINE: str
    DB_URL: PostgresDsn | None = None

    @validator('DB_URL', pre=True)
    def assemble_db_connection(cls, value: str, values: dict) -> str:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme=values.get('DB_ENGINE'),
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    class Config:
        env_file = '.env'


settings = Settings()
