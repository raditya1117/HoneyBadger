from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

https_middleware = Middleware(HTTPSRedirectMiddleware)
