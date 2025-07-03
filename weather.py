# weather.py

from fastapi import FastAPI
import uvicorn
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting FastAPI application...")
app = FastAPI()
logger.info("FastAPI application initialized.")

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"status": "ok", "message": "Minimal FastAPI server is running!"}

if __name__ == "__main__":
    logger.info("Attempting to run Uvicorn server locally...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        logger.critical(f"Fatal error running Uvicorn: {e}", exc_info=True)
