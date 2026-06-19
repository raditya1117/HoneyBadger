from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

trusted_host = Middleware(TrustedHostMiddleware,
                          allowed_hosts=["*"],
                          www_redirect=True)
