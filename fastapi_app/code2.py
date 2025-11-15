from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()


# Define a custom exception class
class InvalidOperationError(Exception):
    def __init__(self, message: str="Not a valid operation.",type: str= "FAILURE", code: int = 404):
        self.message = message
        self.code = code
        self.type=type
        super().__init__(message)


# Register an exception handler to handle the InvalidOperationError exception
@app.exception_handler(InvalidOperationError)
async def invalid_operation_exception_handler(request: Request,exc: InvalidOperationError):
    return JSONResponse(status_code=exc.code, content={"type":exc.type, "reason":exc.message})


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
        try:
            result=num1+num2
        except:
            raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Not able to add {} and {}.".format(num1, num2)})  
    elif operation=="subtract":
        try:
            result=num1-num2
        except:
            raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Not able to subtract {} from {}.".format(num2, num1)})
    elif operation=="multiply":
        try:
            result=num1*num2
        except:
            raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Not able to multiply {} and {}.".format(num1, num2)})
    elif operation=="divide":
        try:
            result=num1/num2
        except:
            raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Not able to divide {} by {}.".format(num1, num2)})
    else:
        result=None
    if result is None:
        raise InvalidOperationError
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})
