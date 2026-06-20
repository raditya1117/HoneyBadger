from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


# Define a function for the root API endpoint
async def root(request: Request):
    return JSONResponse(
        status_code=200,
        content={"type": "METADATA", "output": "Welcome to Calculator by HoneyBadger."},
    )

# Define a function for the calculator API endpoint
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

# Initialize the app
app = Starlette(routes=routes)
