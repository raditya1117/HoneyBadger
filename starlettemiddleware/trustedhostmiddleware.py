from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

trusted_host_middleware = Middleware(TrustedHostMiddleware,
                                     allowed_hosts=["calculator.honeybadger.io",
                                                    "*.honeybadger.io",
                                                    "localhost",
                                                    "127.0.0.1"],
                                     www_redirect=True)
