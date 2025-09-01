"""
Foundation Project - Health Check Router
Health check endpoints for monitoring and load balancers
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import psutil
import os

from ...data.database import get_db
from ...core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "service": "foundation-project-api"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    try:
        # System information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Process information
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "service": "foundation-project-api",
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "memory_total": memory.total,
                "disk_percent": disk.percent,
                "disk_free": disk.free,
                "disk_total": disk.total
            },
            "process": {
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads()
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check - verifies the service is ready to accept traffic"""
    try:
        # Check database connection
        db.execute("SELECT 1")
        
        return {
            "status": "ready",
            "timestamp": time.time(),
            "database": "connected",
            "service": "foundation-project-api"
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get("/health/live")
async def liveness_check():
    """Liveness check - verifies the service is alive and running"""
    try:
        # Basic process check
        process = psutil.Process(os.getpid())
        if not process.is_running():
            raise Exception("Process not running")
        
        return {
            "status": "alive",
            "timestamp": time.time(),
            "pid": os.getpid(),
            "service": "foundation-project-api"
        }
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not alive")

@router.get("/health/metrics")
async def health_metrics():
    """Health metrics in Prometheus format"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Process metrics
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        metrics = f"""# HELP foundation_project_cpu_percent CPU usage percentage
# TYPE foundation_project_cpu_percent gauge
foundation_project_cpu_percent {cpu_percent}

# HELP foundation_project_memory_percent Memory usage percentage
# TYPE foundation_project_memory_percent gauge
foundation_project_memory_percent {memory.percent}

# HELP foundation_project_memory_bytes Memory usage in bytes
# TYPE foundation_project_memory_bytes gauge
foundation_project_memory_bytes {{type="available"}} {memory.available}
foundation_project_memory_bytes {{type="total"}} {memory.total}

# HELP foundation_project_disk_percent Disk usage percentage
# TYPE foundation_project_disk_percent gauge
foundation_project_disk_percent {disk.percent}

# HELP foundation_project_disk_bytes Disk usage in bytes
# TYPE foundation_project_disk_bytes gauge
foundation_project_disk_bytes {{type="free"}} {disk.free}
foundation_project_disk_bytes {{type="total"}} {disk.total}

# HELP foundation_project_process_memory_bytes Process memory usage in bytes
# TYPE foundation_project_process_memory_bytes gauge
foundation_project_process_memory_bytes {{type="rss"}} {process_memory.rss}
foundation_project_process_memory_bytes {{type="vms"}} {process_memory.vms}

# HELP foundation_project_process_threads Process thread count
# TYPE foundation_project_process_threads gauge
foundation_project_process_threads {process.num_threads()}
"""
        
        return metrics
        
    except Exception as e:
        logger.error(f"Health metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Health metrics failed")
