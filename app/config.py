
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        env_prefix="APP_"
    )

    # ------------------------------------------------------------------------------
    # Databases
    # ------------------------------------------------------------------------------

    DB_URL: str = 'sqlite:///db.sqlite'



    # ------------------------------------------------------------------------------
    # Networking
    # ------------------------------------------------------------------------------

    # The port that the server will be operating from
    SERVER_PORT: int = 8000


    # ------------------------------------------------------------------------------
    # OAuth2 Configuration
    # ------------------------------------------------------------------------------

    # Number of bits of entropy to use for generating tokens
    OAUTH2_TOKEN_ENTROPY_BITS: int = 256

    # Number of seconds that an access token is valid
    OAUTH2_ACCESS_TOKEN_TIME_TO_LIVE: int = 8 * 60 * 60


settings = Settings()


