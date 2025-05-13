import os
from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file="../.env",
#         env_file_encoding="utf-8",
#     )


#     POSTGRES_USER: str = os.getenv("POSTGRES_USER", )
#     POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", )
#     POSTGRES_DB: str = os.getenv("POSTGRES_DB", )
#     POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", )
#     POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
#     DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")


#     STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./storage")
#     MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))
#     ALLOWED_EXTENSIONS: set[str] = {".txt"}


# settings = Settings()



import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
    )


    POSTGRES_USER: str = os.getenv("POSTGRES_USER", )
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", )
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", )
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", )
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    SECRET_KEY: str = "supersecret"
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./storage")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))
    ALLOWED_EXTENSIONS: set[str] = {".txt"}


settings = Settings()