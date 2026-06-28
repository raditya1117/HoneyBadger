from fastapi import FastAPI, Request
from starlette.middleware import Middleware


class Tagger:
    def __init__(self, app, name):
        self.app = app
        self.name = name

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        print(f"→ Processing request: {self.name}")

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                print(f"← Processing response:  {self.name}")
            await send(message)

        await self.app(scope, receive, send_wrapper)


# Add middlewares to FastAPI constructor
app = FastAPI(middleware=[
    Middleware(Tagger, name="M1"),
    Middleware(Tagger, name="M2"),
    Middleware(Tagger, name="M3"),
])

# Add middleware using add_middleware
app.add_middleware(Tagger, name="M4")


# Add middleware using decorator
@app.middleware("http")
async def m7(request: Request, call_next):
    print("→ Processing request: M7")
    response = await call_next(request)
    print("← Processing response:  M7")
    return response


# Add middlewares using add_middleware
app.add_middleware(Tagger, name="M5")
app.add_middleware(Tagger, name="M6")


# Add middleware using decorator
@app.middleware("http")
async def m8(request: Request, call_next):
    print("→ Processing request: M8")
    response = await call_next(request)
    print("← Processing response:  M8")
    return response


@app.get("/")
async def root():
    print("   [route handler]")
    return {"ok": True}
