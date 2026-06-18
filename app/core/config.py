from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql+psycopg://vetclinic:vetclinic@postgres:5432/vetclinic"
    APP_NAME: str = "VetClinic API"
    APP_VERSION: str = "1.0.0"


settings = Settings()
