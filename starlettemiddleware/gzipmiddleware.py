from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware

gzip_middleware = Middleware(GZipMiddleware,
                             minimum_size=1024,
                             compress_level=9)
