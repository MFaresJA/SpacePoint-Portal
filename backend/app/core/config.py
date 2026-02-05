from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "SpacePoint Portal API"
    env: str = "dev"

    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "spacepoint"
    postgres_user: str = "spacepoint"
    postgres_password: str = "spacepoint"

    model_config = SettingsConfigDict(
        env_file=".env.dev",  # loaded in local runs; Docker already injects env_file too
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
