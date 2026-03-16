import uvicorn
from fastapi import FastAPI
import logging

from src.api.router import main_router

app = FastAPI()

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    logging.log(20,"listening...")
