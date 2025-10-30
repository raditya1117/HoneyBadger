[gfg](https://www.geeksforgeeks.org/python/error-handling-in-fastapi/)
[medium](https://medium.com/delivus/exception-handling-best-practices-in-python-a-fastapi-perspective-98ede2256870)
[getorchestra](https://www.getorchestra.io/guides/fastapi-mastering-error-handling-with-examples)
[plainenglish](https://python.plainenglish.io/effortless-exception-error-handling-in-fastapi-a-clean-and-simplified-approach-db6f6a7a497c)
[betterstack](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/)

# Error Handling in FastAPI
Errors and exceptions are inevitable in any software and FastAPI applications are no exception. It is imporant to handle errors in a FastAPI applications as errors can disrupt the normal flow of execution, expose sensitive information, and lead to poor user experience. Hence, we need to implement a robust error-handling mechanim in FasAPI applications.
In this article, we will discuss the different types of errors in FastAPI to help you understand their causes and effects. We will also discuss the different ways to implement error handling in FastAPI using in-built methods and custom exception classes. Finally we will discuss some FastAPI error handling best practices to help you build robust APIs.


## What are errors and exceptions in FastAPI?

Errors and exectpions in FastAPI are situations where the normal flow of an application is interrupted due to an unexpected event, such as invalid input, missing data, or a failed database connection. For example, trying to divide a number by zero causes an error as it is not a valid mathematical operation.

FastAPI provides a structured way to handle errors using different exception handling mechanisms. After encountering an error, the FastAPI app raises an exception that disrupts the normal execution flow of the app. We can then catch the exception, log the error messages, and send a meaningful HTTP response to the user.

To understand the diffeerent types and errors in FastAPI and handling them, let's create a calculator app using FastAPI. 

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
In this code, we have defined the `/calculate` endpoint in the FastAPI application that takes the operation name and operands as its input, validates the input using the `InputData` model and returns the calculated value in case of successfull execution.  Save the above code in `calculator_app.py`. Next, run the FastAPI server with the calculator application using the following command:

```bash
uvicorn calculator_app:app --reload --port 8080 --host 0.0.0.0
```
After starting the FastAPI server, you can perform different operations by sending HTTP requests to the server. For example, we can send a GET request to the root API endpoint of the calculator app as follows:
```bash
curl -X GET "http://127.0.0.1:8080/"
```
In response the FastAPI application sends the following output.

```json
{"type":"METADATA","output":"Welcome to Calculator by HoneyBadger."}
```
As the API call is successfully executed, the FastAPI application records it as a successfull execution using the `200 OK` HTTP code.
```py
INFO:     127.0.0.1:57462 - "GET / HTTP/1.1" 200 OK
```
Just like the root API endpoint, you can send a POST request to the `/calculate` endpoint to add two numbers, as shown below:

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "add", "num1":10, "num2": 10}'
```
Executing the above commad will give you the following output.

```json
{"type":"SUCCESS","output":20.0}
```
Again, FastAPI logs the API call as a successfull execution using the HTTP code `200 OK`.
```py
INFO:     127.0.0.1:43880 - "POST /calculate/ HTTP/1.1" 200 OK
```

Now that we have implemented the basic calculator app, let's discuss the differnt errors.

## Different types of errors in FastAPI

Errors in FastAPI are caregorized into various types such as internal server errors, validation errors, and HTTP exceptions. Let's discss the different types of errors in FastAPI so that we can implement mechanisms to handle each of them.

### Internal Server Error

Internal server errors are caused by unexpected runtime issues like logical errors, math errors, or database issues that aren't explicitely handled by the program. For example, if the calculator app running on the FastAPI server tries to divide a number by zero, it will return internal server error due to ZeroDivisionError, as shown in the following example:

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
In this API call, we have passed zero as the second operand. Hence, the server returns `Internal Server Error` as its output. 
```py
Internal Server Error
```
If you look at the execution logs of the FastAPI application, you can see the ZeroDivisionError exception with the message `ZeroDivisionError: float division by zero`.

```py
INFO:     127.0.0.1:46266 - "POST /calculate/ HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/aditya1117/.local/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
.....  
  File "/home/aditya1117/codes/HoneyBadger/fastapi_app/calculator_app.py", line 33, in calculation
    result=num1/num2
ZeroDivisionError: float division by zero
```

After an internal server error, the fastapi server stops and it must be restarted. 

### Method Not Allowed error

The `Method Not Allowed` error occurs due to wrong HTTP method in the API call. If a FastAPI endpoint is defined using the POST request method and we call the API endpoint using GET request method, the FastAPI server run into StarletteHTTPException with status code 405. For instance, we have defined the `/calculate` endpoint using the POST request method. When we send a GET request to the endpoint, the FastAPI app runs into StarletteHTTPException exception. 

```
curl http://127.0.0.1:8080/calculate/ -X GET -H "Content-Type: application/json" -d '{"operation": "add", "num1":10, "num2": 10}'
```

FastAPI internally handles the StarletteHTTPException and returns the `"Method Not Allowed"` message. 
```
{"detail":"Method Not Allowed"}
```
If you check the execution logs, you can see `405 Method Not Allowed` message as follows:
```
INFO:     127.0.0.1:34004 - "GET /calculate/ HTTP/1.1" 405 Method Not Allowed
```


### Request Validation Error

FastAPI validates inputs using pydantic models. If an incoming request for a FastAPI endpoint doesn't conform to the declared structure and parameter types, FastAPI returns request validation error in response. For example, we have defined the /calculate endpoint that with three inputs where the `operation` must be a string and `num1` and `num2` must be floating point numbers or strings that can be converted to floats. When we pass a string that cannot be converted to a floating point number, we run into the request validation error.


```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 'HoneyBadger'}'
```
For the above API call, the FastAPI app returns a json object with "JSON decode error" message.
```json
{"detail":[{"type":"json_invalid","loc":["body",43],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting value"}}]}
```
If you look into the logs, the FastAPI app logs the API calls with request validation errors with the message `422 Unprocessable Entity`. 
```py
INFO:     127.0.0.1:38050 - "POST /calculate/ HTTP/1.1" 422 Unprocessable Entity
```

### HTTP Exception

HTTP exceptions are built-in FastAPI exceptions that we can use to raise exceptions and send error responses with standard HTTP status codes. When we raise an HTTP exception, FastAPI automatially handles the exception and returns the content in the `detail` parameter to as the API response. For instance, we have raised an HTTP exception in our FastAPI app when the requested operation in the API call is other than add, subtract, multiply, and divide. Hence, if we pass `write` as an input to the operation field, the calculator app raises the HTTP exception.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```
In the API response, we get the content from the detail parameter of the exception as the output.

```json
{"detail":{"type":"FAILURE","reason":"Not a valid operation"}}
```
As we have defined the status code in the HTTPException to be 404, FastAPI logs the API execution call with the `404 Not Found` message. 
```py
INFO:     127.0.0.1:53822 - "POST /calculate/ HTTP/1.1" 404 Not Found
```
In addition to built-in errors and exceptions, we can also define custom execeptions based on business logic. Let's discuss how to do so.

### Custom exceptions

We can define custom FastAPI exceptions for handling errors due to business logic by inheriting built-in Python exception classes. In the custom exception, we can define any number of attributes to store the information about the error. After defining the exception, we can create exception handlers to handle the custom exception. 

For example, we can create a custom `InvalidOperationError` exception by inheriting the Python `Exception` class to handle errors due to unsupported `operation` in the API requests to the calculator app. Next, we can create an exception handler using the `@app.exception_handler` decorator to handle the `InvalidOperationError` by raising an HTTPException to get the output for the API call.  

After defining the exception along with the exception handler, we can raise the custom exception from anywhere in the code and it gets handled by the exception handler. 

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
In this code, we have raised InvalidOperationError for API calls with unsupported operations. Now, let's pass `write` as an operation to the /calculate API endpoint.
```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```
The FastAPI application gives the following output as the response for the above request. 
```
{"detail":{"type":"FAILURE","reason":"Not a valid operation."}}
```
As you can see, the handler for the InvalidOperationError raises an HTTPException, which gives us the message output using the attributes of the InvalidOperationError. In the logs, FastAPI records this execution with `404 Not Found` message as we have assigned the 404 HTTP code to the InvalidOperationError.

```
INFO:     127.0.0.1:56798 - "POST /calculate/ HTTP/1.1" 404 Not Found
```
Now that we have discussed different FastAPI errors and custom exceptions, let's discuss how to handle FastAPI errors.

## How to handle errors and exceptions in FastAPI? 

We can use the try-except blocks to manually raise HTTPExceptions with proper messages for different types of errors. We can also define custom exception handlers that handle exceptions of a particular type from the entire application. Finally, we can create a global exception handler that handles any uncaughet exception, preventing the FastAPI exception from falling into an Internal Server Error. Let's discuss all the approces to handle FastAPI errors, starting with Python try-except blocks.

## Error handling using try-except in FastAPI
To handle errors using try-except blocks in a FastAPI application, we can manually handle different types of errors in the except blocks and raise HTTP exceptions with proper message and status code. For example, we can use the try-except blocks to handle errors in our FastAPI application as shown in the following code:

```py
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
```
In this code, we have used try-except blocks to handle errors and raise HTTP exceptions for each operation. We also have the custom exception class with handler for the unsupported operations. Now, let's try to divide a number by zero using the /calculate API call.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
The above API call triggers a ZeroDivisionError exception, which is handled by he except block of the divide operation, and we get the following output in the API response.

```json
{"detail":{"type":"FAILURE","reason":"Not able to divide 10.0 by 0.0."}}
```
In the logs, the above API call is recorded with the message `400 Bad Request` as we have set the status code to 400 while raising the HTTP exception.

```py
INFO:     127.0.0.1:52422 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```

A single exception can occur at multiple places in a program. Also, we might miss putting all the exception types in the except block of the code, which may lead to uncaught errors. We can use custom exception handlers to reduce code repetition and handle errors of a prticular type at one place, regardless of where they originate in the code. Custom exception handles also allow us to format errors of a specific type to follow a standard JSON format. Let's discuss how to handle FastAPI errors using custom exception handlers. 

## Error handling using custom exception handlers in FastAPI

FastAPI allows us to write custom handlers for each exception using the `exception_handler` decorator. Each custom exception handler takes the request object and an exception as its input. 

```py
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
        super().__init__(self.message)

# Register an exception handler to handle the InvalidOperationError exception
@app.exception_handler(InvalidOperationError)
async def invalid_operation_exception_handler(request: Request,exc: InvalidOperationError):
    raise HTTPException(status_code=exc.code, detail={"type":exc.type, "reason":exc.message})

# Register an exception handler to handle the TypeError exception
@app.exception_handler(TypeError)
async def typeerror_handler(request: Request, exc: TypeError):
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"TypeError exception occurred due to mismatch between the expected and the actual data type of the operands."})

# Register an exception handler to handle the ZeroDivisionError exception
@app.exception_handler(ZeroDivisionError)
async def zerodivisionerror_handler(request: Request,exc: ZeroDivisionError):
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"Cannot perform division as the second operand is zero."})

# Register an exception handler to handle the ValueError exception
@app.exception_handler(ValueError)
async def zerodivisionerror_handler(request: Request,exc: ValueError):
    raise HTTPException(status_code=400, detail={"type":"FAILURE", "reason":"ValueError exception occurred due to operands with correct data types but inappropriate values."})

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
```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'```
```
```json
{"detail":{"type":"FAILURE","reason":"Cannot perform division as the second operand is zero."}}
```
```py
INFO:     127.0.0.1:50036 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```

```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":1e308, "num2": 1e-100}'
```
```
{"detail":{"type":"FAILURE","reason":"ValueError exception occurred due to operands with correct data types but inappropriate values."}}
```

```
INFO:     127.0.0.1:41754 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```
We can also pass the content in the request to the  jhdsf

```
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
```
```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```
```
{"detail":{"type":"FAILURE","reason":"Not a valid operation.","operand_1":10.0,"operand_2":10.0,"operation":"write"}}
```
```
INFO:     127.0.0.1:34688 - "POST /calculate/ HTTP/1.1" 404 Not Found
```

```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
```
{"detail":{"type":"FAILURE","reason":"Cannot perform division as the second operand is zero.","operand_1":10.0,"operand_2":0.0,"operation":"divide"}}
```
```
INFO:     127.0.0.1:38138 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```
## Using a global exception handler in FastAPI

This section will discuss implementing a global FastAPI exception handler.

```py
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

# Register an exception handler to handle rest of the errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request,exc: Exception):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    raise HTTPException(status_code=500, detail={"type":"FAILURE", "reason":"An unexpected error occurred.", "operand_1":num1, "operand_2":num2, "operation":operation})

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
```

## FastAPI error handling best practices
This section will discuss some FastAPI error-handling best practices.

## Conclusion
This section will summarize what the article discussed and include a CTA.

## Frequently asked questions

To improve SEO visibility, we will include some FAQs from the Google search page's "people also asked " section.
