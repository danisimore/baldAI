from config.base_config import BaseConfig


class DBConfig(BaseConfig):
    """DB settings."""

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
