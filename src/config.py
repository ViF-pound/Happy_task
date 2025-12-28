from pathlib import Path
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings


BASE_DIR  = Path(__file__).parent.parent


class AuthData(BaseModel):
    
    private_key: Path = BASE_DIR / "src" / "app_auth" / "tokens" / "private_key.pem"
    public_key: Path = BASE_DIR / "src" / "app_auth" / "tokens" / "public_key.pem"
    algorithm: str = "RS256"
    days: int = 31


class EnvData(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = ConfigDict(
        env_file='.env',
        extra='allow'
    )


class Settings(BaseModel):

    auth_data: AuthData = AuthData()
    env_data: EnvData = EnvData()

config = Settings()