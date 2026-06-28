from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import time
from fastapi import Request

app = FastAPI()


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response


# Define the root API endpoint
@app.get("/")
async def root():
    return JSONResponse(status_code=200,
                        content={"type": "METADATA", "output": "Welcome to Calculator by HoneyBadger."})


# Define the input data model
class InputData(BaseModel):
    num1: float
    num2: float
    operation: str


# Define the calculator API endpoint
@app.post("/calculate/")
async def calculation(input_data: InputData):
    num1 = input_data.num1
    num2 = input_data.num2
    operation = input_data.operation
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2
    else:
        result = None
    if result is None:
        raise HTTPException(status_code=404, detail={"type": "FAILURE", "reason": "Not a valid operation"})
    else:
        return JSONResponse(status_code=200, content={"type": "SUCCESS", "output": result})
