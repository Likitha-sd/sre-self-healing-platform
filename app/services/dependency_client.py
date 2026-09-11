import os
import time

import httpx

from app.circuit_breaker import CircuitBreaker


DEPENDENCY_URL = os.getenv("DEPENDENCY_URL", "http://127.0.0.1:8001")
TIMEOUT_SECONDS = 2.0
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5


circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=5,
)


def get_dependency_data():
    if not circuit_breaker.can_execute():
        return None, "circuit_open"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.get(
                f"{DEPENDENCY_URL}/data",
                timeout=TIMEOUT_SECONDS,
            )

            response.raise_for_status()

            circuit_breaker.record_success()

            return response.json(), None

        except httpx.RequestError:
            if attempt == MAX_RETRIES:
                circuit_breaker.record_failure()
                return None, "unavailable"

            time.sleep(RETRY_DELAY_SECONDS)

        except httpx.HTTPStatusError:
            circuit_breaker.record_failure()
            return None, "dependency_error"

    return None, "unavailable"
