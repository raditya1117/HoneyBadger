[gfg](https://www.geeksforgeeks.org/python/error-handling-in-fastapi/)
[medium](https://medium.com/delivus/exception-handling-best-practices-in-python-a-fastapi-perspective-98ede2256870)
[getorchestra](https://www.getorchestra.io/guides/fastapi-mastering-error-handling-with-examples)
[plainenglish](https://python.plainenglish.io/effortless-exception-error-handling-in-fastapi-a-clean-and-simplified-approach-db6f6a7a497c)
[betterstack](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/)

# Error Handling in FastAPI
Errors and exceptions are inevitable in any software and FastAPI applications are no exception. It is imporant to handle errors in a FastAPI applications as errors can disrupt the normal flow of execution, expose sensitive information, and lead to poor user experience. Hence, we need to implement a robust error-handling mechanim in FasAPI applications.
In this article, we will discuss the different types of errors in FastAPI to help you understand their causes and effects. We will also discuss the different ways to implement error handling in FastAPI using in-built methods and custom exception classes. Finally we will discuss some FastAPI error handling best practices to help you build robust APIs.


## What are errors and exceptions in FastAPI?

Errors and exectpions in FastAPI are situations where the normal flow of an application is interrupted due to an unexpected event like invalid input, missing data, or a failed database connection. Errors are caused due to problems in the application logic that prevenets the FastAPI app to execute. For example, trying to divide a number by zero causes an error. 
FastAPI provides a structured way to handle errors using different exception handling mechanisms. In case of an error, the program raises an exception that disrupts the normal execution flow of the FastAPI app. We can then catch the exception, log the error messages, and send a meaningful HTTP response for the given error. 

```py
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
        raise HTTPException(status_code=404, detail={"type":"FAILURE", "reason":"Not a valid operation"})
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})
```
Curl command:

```bash
uvicorn app1:app --reload --port 8080 --host 0.0.0.0
```

```bash
curl -X GET "http://127.0.0.1:8080/"
```
Output:

```json
{"type":"METADATA","output":"Welcome to Calculator by HoneyBadger."}
```
logs:

```py
INFO:     127.0.0.1:57312 - "GET / HTTP/1.1" 200 OK
```

Similarly, you can use the curl command to add two numbers as shown below:

curl command
```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "add", "num1":10, "num2": 10}'
```
output

```json
{"type":"SUCCESS","output":20.0}
```
logs
```py
INFO:     127.0.0.1:34394 - "POST /calculate/ HTTP/1.1" 200 OK
```
Now that we have implemented the basic calculator app, let's discuss the differnt errors.
## Different types of errors in FastAPI

Errors in FastAPI are caregorized into various types such as internal server errors, validation errors, and HTTP exceptions. Let's discss the different types of errors in FastAPI so that we can implement mechanisms to handle each of them.

### Internal Server Error
Internal server errors are caused by unexpected runtime issues like logical errors, math errors, or database issues that aren't explicitely handled by the program. For example, if the calculator app running on the FastAPI server tries to divide a number by zero, it will return internal server error due to ZeroDivisionError, as shown in the following example.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```

OUtout:
```py
Internal Server Error
```

Logs
```py
INFO:     127.0.0.1:46266 - "POST /calculate/ HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/aditya1117/.local/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
.....  
  File "/home/aditya1117/codes/HoneyBadger/fastapi_app/app1.py", line 33, in calculation
    result=num1/num2
ZeroDivisionError: float division by zero

```
After an internal server error, the fastapi server stops and you need to restart it.

### Request Validation Error
FastAPI validates inputs using pydantic models. If an incoming request for a FastAPI server endpoint doesn't coform to the declared structure and parameter types, FastAPI returns request validation error in response.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 'Aditya'}'
```
Output:
```json
{"detail":[{"type":"json_invalid","loc":["body",43],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting value"}}]}
```
logs:

```py
INFO:     127.0.0.1:53514 - "POST /calculate/ HTTP/1.1" 422 Unprocessable Entity
```

### HTTP Exception

HTTP exceptions are built-in FastAPI exceptions that we can use to raise exceptions and send error responses with standard HTTP status codes. 

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```

outout
```json
{"detail":{"type":"FAILURE","reason":"Not a valid operation"}}
```
logs

```py
INFO:     127.0.0.1:43230 - "POST /calculate/ HTTP/1.1" 404 Not Found
```

### Custom exceptions

 We can also define custom FastAPI exceptions by inheriting built-in FastAPI exceptions. AFter defining the exception, we can register exception handlers using the `@app.exception_handler` decorator to handle the exception. For example, 

```py
from fastapi import FastAPI, HTTPException,Request
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
        raise InvalidOperationError
    else:
        return JSONResponse(status_code=200, content={"type":"SUCCESS", "output":result})
```

```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```

```
{"detail":{"type":"FAILURE","reason":"Not a valid operation."}}
```

After discussing the different FastAPI errors, we will discuss handling exceptions using different methods.

## Error handling using try-except in FastAPI

This section will discuss how to handle FastAPI errors using try-except blocks.

```py
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
```

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
output
```json
{"type":"FAILURE","reason":"Not able to divide 10.0 by 0.0."}
```
logs
```py
INFO:     127.0.0.1:34956 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```

## Error handling using FastAPI HTTPException
This section will discuss handling FastAPI errors using the HTTPException exception class.

## Custom exception handling in FastAPI
This section will discuss implementing custom exception classes to handle FastAPI errors.

## Using a global exception handler in FastAPI

This section will discuss implementing a global FastAPI exception handler.

## FastAPI error handling best practices
This section will discuss some FastAPI error-handling best practices.

## Conclusion
This section will summarize what the article discussed and include a CTA.

## Frequently asked questions

To improve SEO visibility, we will include some FAQs from the Google search page's "people also asked " section.
