from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Define a CORSMiddleware
cors_middleware = Middleware(CORSMiddleware,
                             allow_origins=["*"],
                             allow_methods=["GET", "POST"],
                             allow_headers=["Content-Type", "X-API-Key"],
                             expose_headers=["X-Request-ID"],
                             allow_credentials=True,
                             max_age=3600)
