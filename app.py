#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from routes.document import document_router
from exceptions.ServerException import ServerException

import os
import uvicorn

load_dotenv()

API_KEY = os.getenv("API_KEY", None)

if not API_KEY:
    raise HTTPException(
        status_code=402,
        detail="Not set api key"
    )

app = FastAPI()

@app.exception_handler(ServerException)
async def server_exception_handler(request, exc: ServerException):
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


app.include_router(document_router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        reload=True
        )







