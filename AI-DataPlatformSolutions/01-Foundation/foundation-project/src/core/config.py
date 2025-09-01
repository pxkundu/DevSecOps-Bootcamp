"""
Foundation Project - Configuration Management
Environment-based configuration with validation
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator, Field
from pydantic.types import SecretStr

class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    name: str = Field(default="foundation_project", env="DB_NAME")
    user: str = Field(default="postgres", env="DB_USER")
    password: SecretStr = Field(default="password", env="DB_PASSWORD")
    pool_size: int = Field(default=20, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=30, env="DB_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="DB_ECHO")
    
    @property
    def url(self) -> str:
        """Get database connection URL"""
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
    
    class Config:
        env_prefix = "DB_"

class RedisSettings(BaseSettings):
    """Redis configuration settings"""
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    password: Optional[SecretStr] = Field(default=None, env="REDIS_PASSWORD")
    db: int = Field(default=0, env="REDIS_DB")
    pool_size: int = Field(default=10, env="REDIS_POOL_SIZE")
    
    @property
    def url(self) -> str:
        """Get Redis connection URL"""
        if self.password:
            return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
    
    class Config:
        env_prefix = "REDIS_"

class SecuritySettings(BaseSettings):
    """Security configuration settings"""
    secret_key: SecretStr = Field(env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")
    allowed_hosts: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        if len(v.get_secret_value()) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    class Config:
        env_prefix = "SECURITY_"

class MLflowSettings(BaseSettings):
    """MLflow configuration settings"""
    tracking_uri: str = Field(default="http://localhost:5000", env="MLFLOW_TRACKING_URI")
    registry_uri: str = Field(default="http://localhost:5000", env="MLFLOW_REGISTRY_URI")
    experiment_name: str = Field(default="foundation_project", env="MLFLOW_EXPERIMENT_NAME")
    
    class Config:
        env_prefix = "MLFLOW_"

class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings"""
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    grafana_port: int = Field(default=3000, env="GRAFANA_PORT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    enable_tracing: bool = Field(default=True, env="ENABLE_TRACING")
    
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    class Config:
        env_prefix = "MONITORING_"

class Settings(BaseSettings):
    """Main application settings"""
    # Application
    app_name: str = Field(default="Foundation Project", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # Database
    database: DatabaseSettings = DatabaseSettings()
    
    # Redis
    redis: RedisSettings = RedisSettings()
    
    # Security
    security: SecuritySettings = SecuritySettings()
    
    # MLflow
    mlflow: MLflowSettings = MLflowSettings()
    
    # Monitoring
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # Computed properties
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() in ["development", "dev", "local"]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() in ["production", "prod"]
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.environment.lower() in ["testing", "test"]
    
    @property
    def allowed_hosts(self) -> List[str]:
        """Get allowed hosts for CORS and trusted host middleware"""
        return self.security.allowed_hosts
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins"""
        return self.security.cors_origins
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Environment-specific overrides
if settings.is_development:
    # Development overrides
    settings.debug = True
    settings.monitoring.log_level = "DEBUG"
    
elif settings.is_production:
    # Production overrides
    settings.debug = False
    settings.monitoring.log_level = "WARNING"
    
    # Ensure production security
    if settings.security.allowed_hosts == ["*"]:
        settings.security.allowed_hosts = ["localhost", "127.0.0.1"]
    
    if settings.security.cors_origins == ["*"]:
        settings.security.cors_origins = ["https://yourdomain.com"]

# Validation
def validate_settings():
    """Validate all settings and raise errors if invalid"""
    try:
        # Test database connection string
        _ = settings.database.url
        
        # Test Redis connection string
        _ = settings.redis.url
        
        # Validate secret key
        _ = settings.security.secret_key.get_secret_value()
        
        return True
    except Exception as e:
        raise ValueError(f"Invalid configuration: {e}")

# Validate settings on import
if __name__ != "__main__":
    validate_settings()
