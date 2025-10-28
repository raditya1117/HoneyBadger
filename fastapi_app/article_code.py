from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()

# Define a custom exception class
class InvalidOperationError(Exception):
    def __init__(self, message: str="Not a valid operation.",type: str= "FAILURE", code: int = 404):
        self.message = message
        self.code = code
        self.type=type
        super().__init__(self.message)

# Register an exception handler to handle the InvalidOperationError exception
@app.exception_handler(InvalidOperationError)
async def invalid_operation_exception_handler(request: Request,exc: InvalidOperationError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    raise HTTPException(status_code=exc.code, detail={"type":exc.type, "reason":exc.message, "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the TypeError exception
@app.exception_handler(TypeError)
async def typeerror_handler(request: Request,exc: TypeError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"TypeError exception occurred due to mismatch between the expected and the actual data type of the operands.", "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the ZeroDivisionError exception
@app.exception_handler(ZeroDivisionError)
async def zerodivisionerror_handler(request: Request,exc: ZeroDivisionError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Cannot perform division as the second operand is zero.", "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the ValueError exception
@app.exception_handler(ValueError)
async def zerodivisionerror_handler(request: Request,exc: ValueError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"ValueError exception occurred due to operands with correct data types but inappropriate values.", "operand_1":num1, "operand_2":num2, "operation":operation})

# Define the root API endpoint
@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"type":"METADATA", "output": "Welcome to Calculator by HoneyBadger."})


# Define the input data model
class InputData(BaseModel):
    num1: float
    num2: float
    operation: str

# Dependency that attaches the validated payload to request.state
async def attach_payload(payload: InputData, request: Request = None):
    request.state.payload = payload
    return payload

# Define the calculator API endpoint
@app.post("/calculate/")
async def calculation(input_data: InputData = Depends(attach_payload)):
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
        raise InvalidOperationError
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})