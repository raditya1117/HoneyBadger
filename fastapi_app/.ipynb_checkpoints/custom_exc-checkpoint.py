from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()


# Define a custom exception class
class InvalidOperationError(Exception):
    def __init__(self, type: str= "FAILURE", message: str, code: int = 404):
        self.message = message
        self.code = code
        self.type=type
        super().__init__(message)


# Register an exception handler to handle the custom exception
@app.exception_handler(InvalidOperationError)
async def zerodivision_exception_handler(exc: InvalidOperationError):
    raise HTTPException(status_code=exc.code, detail={"type":exc.type, "reason":exc.message})

# Define the root API endpoint
@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"type":"METADATA", "output": "Welcome to Calculator by HoneyBadger."})


# Define the input data model
class InputData(BaseModel):
    num1: float
    num2: float
    operation: str

# Define the calculator API endpoint
@app.post("/calculate/")
async def calculation(input_data: InputData):
    num1=input_data.num1
    num2=input_data.num2
    operation=input_data.operation
    if operation=="add":
        result=num1+num2
    elif operation=="subtract":
        result=num1-num2
    elif operation=="multiply":
        result=num1*num2
    elif operation=="divide":
        result=num1/num2
    else:
        result=None
    if result is None:
        raise InvalidOperationError(type="FAILURE",message="Not a valid operation.", code="404")
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})
