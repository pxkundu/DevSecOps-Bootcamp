#!/usr/bin/env python3
"""
Foundation Project - Startup Script
Simple script to run the Foundation Project API
"""

import uvicorn
import os
from pathlib import Path

def main():
    """Main startup function"""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Change to project root
    os.chdir(project_root)
    
    # Configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    workers = int(os.getenv("API_WORKERS", "1"))
    
    print(f"🚀 Starting Foundation Project API")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"👥 Workers: {workers}")
    print(f"📁 Project Root: {project_root}")
    
    # Start the server
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_level="info"
    )

if __name__ == "__main__":
    main()
