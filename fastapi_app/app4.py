from fastapi import FastAPI,Request,Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse

#uvicorn fastapi_app:app1 --reload --port 8080 --host 0.0.0.0
# curl -X GET "http://127.0.0.1:8080/"
app = FastAPI()


# Define the input data model
class InputData(BaseModel):
    num1: int
    num2: int
    operation: str

# Dependency that attaches the validated payload to request.state
async def attach_payload(payload: InputData, request: Request = None):
    # store the validated model on the request for exception handlers
    request.state.payload = payload
    return payload
    

@app.exception_handler(ZeroDivisionError)
async def zerodivision_exception_handler(request: Request, exc: ZeroDivisionError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    return JSONResponse(
        status_code=400,
        content={
            "message": {
                "type": "FAILURE",
                "reason": f"Not able to divide {num1} by {num2}."
            }
        }
    )



@app.get("/")
async def read_root():
    return {"message": "Welcome."}




@app.post("/calculate/")
async def calculation(input_data: InputData= Depends(attach_payload)):
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
        result=num1/str(num2)
    else:
        result=None
    if result is None:
        return {"type":"FAILURE", "reason":"Not a valid operation"}
    else:
        return {"type":"SUCCESS", "output":result}
        
