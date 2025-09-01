"""
Foundation Project - Database Models
SQLAlchemy models for the foundation project
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, JSON, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class User(Base, TimestampMixin):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    data_sources = relationship("DataSource", back_populates="owner", cascade="all, delete-orphan")
    ml_models = relationship("MLModel", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Role(Base, TimestampMixin):
    """Role model for role-based access control"""
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, nullable=True)  # Store permissions as JSON
    
    # Relationships
    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

class UserRole(Base, TimestampMixin):
    """User-Role association table"""
    __tablename__ = "user_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_roles")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
        Index('idx_user_role_user_id', 'user_id'),
        Index('idx_user_role_role_id', 'role_id'),
    )
    
    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"

class DataSource(Base, TimestampMixin):
    """Data source model for managing data inputs"""
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=False, index=True)  # database, api, file, stream
    connection_config = Column(JSON, nullable=False)  # Connection details
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    sync_frequency = Column(String(50), nullable=True)  # daily, hourly, real-time
    
    # Relationships
    owner = relationship("User", back_populates="data_sources")
    datasets = relationship("Dataset", back_populates="data_source", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.source_type}')>"

class Dataset(Base, TimestampMixin):
    """Dataset model for managing data collections"""
    __tablename__ = "datasets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data_source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False)
    schema_version = Column(String(20), nullable=False, default="1.0")
    row_count = Column(Integer, nullable=True)
    size_bytes = Column(BigInteger, nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Relationships
    data_source = relationship("DataSource", back_populates="datasets")
    features = relationship("Feature", back_populates="dataset", cascade="all, delete-orphan")
    ml_models = relationship("MLModel", back_populates="training_dataset", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dataset(id={self.id}, name='{self.name}', source_id={self.data_source_id})>"

class Feature(Base, TimestampMixin):
    """Feature model for ML features"""
    __tablename__ = "features"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=False)
    data_type = Column(String(50), nullable=False)  # numeric, categorical, text, datetime
    is_target = Column(Boolean, default=False, nullable=False)
    is_required = Column(Boolean, default=True, nullable=False)
    validation_rules = Column(JSON, nullable=True)  # Validation constraints
    statistics = Column(JSON, nullable=True)  # Feature statistics
    
    # Relationships
    dataset = relationship("Dataset", back_populates="features")
    
    def __repr__(self):
        return f"<Feature(id={self.id}, name='{self.name}', type='{self.data_type}')>"

class MLModel(Base, TimestampMixin):
    """ML model model for managing machine learning models"""
    __tablename__ = "ml_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    model_type = Column(String(50), nullable=False, index=True)  # classification, regression, clustering
    algorithm = Column(String(100), nullable=False)  # RandomForest, XGBoost, etc.
    version = Column(String(20), nullable=False, default="1.0.0")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    training_dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=True)
    model_path = Column(String(500), nullable=True)  # Path to model file
    hyperparameters = Column(JSON, nullable=True)  # Model hyperparameters
    metrics = Column(JSON, nullable=True)  # Model performance metrics
    is_active = Column(Boolean, default=True, nullable=False)
    is_production = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="ml_models")
    training_dataset = relationship("Dataset", back_populates="ml_models")
    deployments = relationship("ModelDeployment", back_populates="model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MLModel(id={self.id}, name='{self.name}', type='{self.model_type}')>"

class ModelDeployment(Base, TimestampMixin):
    """Model deployment model for managing model deployments"""
    __tablename__ = "model_deployments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ml_models.id"), nullable=False)
    environment = Column(String(50), nullable=False, index=True)  # staging, production
    status = Column(String(50), nullable=False, default="deployed")  # deployed, failed, stopped
    deployment_config = Column(JSON, nullable=True)  # Deployment configuration
    endpoint_url = Column(String(500), nullable=True)  # Model endpoint URL
    replicas = Column(Integer, default=1, nullable=False)
    resources = Column(JSON, nullable=True)  # Resource requirements
    health_status = Column(String(50), default="healthy", nullable=False)
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    model = relationship("MLModel", back_populates="deployments")
    
    def __repr__(self):
        return f"<ModelDeployment(id={self.id}, model_id={self.model_id}, environment='{self.environment}')>"

class AuditLog(Base, TimestampMixin):
    """Audit log model for tracking system activities"""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    details = Column(JSON, nullable=True)  # Additional action details
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_log_timestamp', 'created_at'),
        Index('idx_audit_log_user_action', 'user_id', 'action'),
        Index('idx_audit_log_resource', 'resource_type', 'resource_id'),
    )
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"

class SystemMetrics(Base, TimestampMixin):
    """System metrics model for monitoring"""
    __tablename__ = "system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20), nullable=True)
    labels = Column(JSON, nullable=True)  # Metric labels/tags
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_system_metrics_name_timestamp', 'metric_name', 'timestamp'),
        Index('idx_system_metrics_timestamp', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<SystemMetrics(id={self.id}, name='{self.metric_name}', value={self.metric_value})>"

# Import BigInteger for large numbers
from sqlalchemy import BigInteger

# Add BigInteger import to the top of the file
__all__ = [
    "Base", "User", "Role", "UserRole", "DataSource", "Dataset", 
    "Feature", "MLModel", "ModelDeployment", "AuditLog", "SystemMetrics"
]
