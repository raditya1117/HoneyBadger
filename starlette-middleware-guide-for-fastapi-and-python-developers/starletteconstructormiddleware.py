from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.middleware import Middleware
import time


# Define a function for the root API endpoint
async def root(request: Request):
    return JSONResponse(
        status_code=200,
        content={"type": "METADATA", "output": "Welcome to Calculator by HoneyBadger."},
    )


# Define a function for the calculate API endpoint
async def calculation(request: Request):
    data = await request.json()
    num1, num2, operation = data["num1"], data["num2"], data["operation"]
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2
    else:
        return JSONResponse(
            status_code=404,
            content={"type": "FAILURE", "reason": "Not a valid operation"},
        )
    return JSONResponse(status_code=200, content={"type": "SUCCESS", "output": result})


# Define the API endpoints
routes = [
    Route("/", root),
    Route("/calculate/", calculation, methods=["POST"]),
]


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{duration:.4f}s"
        return response


cors_middleware = Middleware(CORSMiddleware,
                             allow_origins=["*"],
                             allow_methods=["GET", "POST"],
                             allow_headers=["Content-Type", "X-API-Key"],
                             expose_headers=["X-Request-ID"],
                             allow_credentials=False,
                             max_age=3600)
timing_middleware = Middleware(TimingMiddleware)
# Initialize the app
app = Starlette(routes=routes, middleware=[cors_middleware, timing_middleware])
