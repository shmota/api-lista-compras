from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote

class Settings(BaseSettings):
    app_name: str = "api-lista-compras"
    version: str = "0.0.1"
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    
    @property
    def DATABASE_URL(self):
      return(
        f"postgresql+psycopg://{self.DB_USER}:{quote(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}".replace("%", "%%")
      )
      

    # Optional: load from a .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
print(settings.app_name)