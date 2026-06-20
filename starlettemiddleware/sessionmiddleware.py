from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

session_middleware = Middleware(SessionMiddleware,
                                secret_key="honeybadger-secret-key",
                                session_cookie="calculator_session",
                                max_age=3600,
                                https_only=True,
                                same_site="lax",
                                domain=None,
                                path="/")
