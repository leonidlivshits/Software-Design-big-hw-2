# import os
# #from pydantic_core import Url as AnyUrl
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#     )

#     POSTGRES_USER: str = os.getenv("POSTGRES_USER", )
#     POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", )
#     POSTGRES_DB: str = os.getenv("POSTGRES_DB", )
#     POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", )
#     POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

#     SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
#     DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")


# settings = Settings()



import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


    POSTGRES_USER: str = os.getenv("POSTGRES_USER", )
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", )
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", )
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", )
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    SECRET_KEY: str = "supersecret"


settings = Settings()


