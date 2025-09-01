"""
Foundation Project - Data Router
Data source and dataset management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ...core.security import get_current_user
from ...data.database import get_db
from ...data.models import DataSource, Dataset, User
from ...core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Pydantic models
class DataSourceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # database, file, api, stream
    connection_string: Optional[str] = None
    config: Optional[dict] = None

class DataSourceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    type: str
    connection_string: Optional[str]
    config: Optional[dict]
    owner_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data_source_id: str
    schema: Optional[dict] = None
    metadata: Optional[dict] = None

class DatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    data_source_id: str
    schema: Optional[dict]
    metadata: Optional[dict]
    owner_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.post("/data/sources", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_data_source(
    data_source: DataSourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new data source"""
    try:
        db_data_source = DataSource(
            name=data_source.name,
            description=data_source.description,
            type=data_source.type,
            connection_string=data_source.connection_string,
            config=data_source.config,
            owner_id=current_user.id
        )
        
        db.add(db_data_source)
        db.commit()
        db.refresh(db_data_source)
        
        logger.info(f"Data source created: {data_source.name}")
        return db_data_source
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating data source: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating data source"
        )

@router.get("/data/sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List data sources for current user"""
    data_sources = db.query(DataSource).filter(
        DataSource.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return data_sources

@router.get("/data/sources/{source_id}", response_model=DataSourceResponse)
async def get_data_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific data source"""
    data_source = db.query(DataSource).filter(
        DataSource.id == source_id,
        DataSource.owner_id == current_user.id
    ).first()
    
    if not data_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    return data_source

@router.post("/data/datasets", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new dataset"""
    try:
        # Verify data source exists and user has access
        data_source = db.query(DataSource).filter(
            DataSource.id == dataset.data_source_id,
            DataSource.owner_id == current_user.id
        ).first()
        
        if not data_source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data source not found"
            )
        
        db_dataset = Dataset(
            name=dataset.name,
            description=dataset.description,
            data_source_id=dataset.data_source_id,
            schema=dataset.schema,
            metadata=dataset.metadata,
            owner_id=current_user.id
        )
        
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        
        logger.info(f"Dataset created: {dataset.name}")
        return db_dataset
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating dataset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating dataset"
        )

@router.get("/data/datasets", response_model=List[DatasetResponse])
async def list_datasets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List datasets for current user"""
    datasets = db.query(Dataset).filter(
        Dataset.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return datasets

@router.get("/data/datasets/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific dataset"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    return dataset
