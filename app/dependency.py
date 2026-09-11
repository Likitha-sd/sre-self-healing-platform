import time

from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/data")
def data():
    return {"message": "Dependency is working"}


@app.get("/slow")
def slow():
    time.sleep(5)
    return {"message": "Dependency responded slowly"}


@app.get("/fail")
def fail():
    return JSONResponse(
        content={"error": "Dependency failure"},
        status_code=500
    )
