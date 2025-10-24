from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()

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
            return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Not able to add {} and {}.".format(num1, num2)})  
    elif operation=="subtract":
        try:
            result=num1-num2
        except:
            return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Not able to subtract {} from {}.".format(num2, num1)})
    elif operation=="multiply":
        try:
            result=num1*num2
        except:
            return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Not able to multiply {} and {}.".format(num1, num2)})
    elif operation=="divide":
        try:
            result=num1/num2
        except:
            return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Not able to divide {} by {}.".format(num1, num2)})
    else:
        result=None
    if result is None:
        raise HTTPException(status_code=404, detail={"type":"FAILURE", "reason":"Not a valid operation"})
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})