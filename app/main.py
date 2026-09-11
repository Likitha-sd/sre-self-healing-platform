import time

import httpx

from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import JSONResponse, Response

from app.circuit_breaker import CircuitBreaker
from app.api.routes import router as item_router
from app.database.database import initialize_database


app = FastAPI()
initialize_database()
app.include_router(item_router)

DEPENDENCY_URL = "http://dependency:8001"

TIMEOUT_SECONDS = 2.0
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5

circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=5
)


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)
REQUESTS_BY_STATUS = Counter(
    "http_requests_by_status_total",
    "Total HTTP requests by status code",
    ["method", "endpoint", "status_code"]
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        request.method,
        request.url.path
    ).inc()

    REQUEST_LATENCY.labels(
        request.method,
        request.url.path
    ).observe(duration)

    REQUESTS_BY_STATUS.labels(
        request.method,
        request.url.path,
        str(response.status_code)
    ).inc()

    return response


@app.get("/")
def root():
    return {"message": "Self-Healing Production Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    if circuit_breaker.state == "OPEN":
        return JSONResponse(
            content={"status": "not ready"},
            status_code=503
        )

    return {"status": "ready"}


@app.get("/data")
def get_data():

    if not circuit_breaker.can_execute():
        return JSONResponse(
            content={
                "status": "degraded",
                "message": "Circuit breaker is open"
            },
            status_code=503
        )

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            response = httpx.get(
                f"{DEPENDENCY_URL}/data",
                timeout=TIMEOUT_SECONDS
            )

            response.raise_for_status()

            circuit_breaker.record_success()

            return response.json()

        except httpx.RequestError:

            if attempt == MAX_RETRIES:
                circuit_breaker.record_failure()

                return JSONResponse(
                    content={
                        "status": "degraded",
                        "message": "Dependency unavailable"
                    },
                    status_code=503
                )

            time.sleep(RETRY_DELAY_SECONDS)

        except httpx.HTTPStatusError:

            circuit_breaker.record_failure()

            return JSONResponse(
                content={
                    "status": "degraded",
                    "message": "Dependency returned an error"
                },
                status_code=503
            )

@app.get("/cpu")
def cpu_load():
    total = 0
    for i in range(10_000_000):
        total += i * i
    return {"result": total}

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
