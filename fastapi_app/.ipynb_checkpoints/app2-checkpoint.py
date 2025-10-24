from fastapi import FastAPI
from pydantic import BaseModel

#uvicorn fastapi_app:app1 --reload --port 8080 --host 0.0.0.0
# curl -X GET "http://127.0.0.1:8080/"
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome."}


# Define the input data model
class InputData(BaseModel):
    num1: int
    num2: int
    operation: str

@app.post("/calculate/")
async def calculation(input_data: InputData):
    num1=input_data.num1
    num2=input_data.num2
    operation=input_data.operation
    if operation=="add":
        try:
            result=num1+num2
        except:
            return {"type":"FAILURE", "reason":"Not able to add {} and {}.".format(num1, num2)}
    elif operation=="subtract":
        try:
            result=num1-num2
        except:
            return {"type":"FAILURE", "reason":"Not able to subtract {} from {}.".format(num2, num1)}
    elif operation=="multiply":
        try:
            result=num1*num2
        except:
            return {"type":"FAILURE", "reason":"Not able to multiply {} and {}.".format(num1, num2)}
    elif operation=="divide":
        try:
            result=num1/num2
        except:
            return {"type":"FAILURE", "reason":"Not able to divide {} by {}.".format(num1, num2)}
    else:
        result=None
    if result is None:
        return {"type":"FAILURE", "reason":"Not a valid operation"}
    else:
        return {"type":"SUCCESS", "output":result}
        
