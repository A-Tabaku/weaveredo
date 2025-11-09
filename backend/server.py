"""
Main FastAPI server entry point for Weave
Exposes the API from api/server.py
"""

from api.server import app

# This allows uvicorn to import 'app' from this module
# The actual FastAPI app is defined in api/server.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
