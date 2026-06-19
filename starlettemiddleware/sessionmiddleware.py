from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

session_middleware = Middleware(SessionMiddleware,
                                secret_key="",
                                session_cookie="",
                                max_age="",
                                https_only=False,
                                same_site="Lax",
                                domain=None,
                                path="/")
