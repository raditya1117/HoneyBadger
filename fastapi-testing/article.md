[gfg](https://www.geeksforgeeks.org/python/error-handling-in-fastapi/)
[medium](https://medium.com/delivus/exception-handling-best-practices-in-python-a-fastapi-perspective-98ede2256870)
[getorchestra](https://www.getorchestra.io/guides/fastapi-mastering-error-handling-with-examples)
[plainenglish](https://python.plainenglish.io/effortless-exception-error-handling-in-fastapi-a-clean-and-simplified-approach-db6f6a7a497c)
[betterstack](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/)

# Error Handling in FastAPI
Errors and exceptions are inevitable in any software and FastAPI applications are no exception. It is imporant to handle errors in FastAPI applications as errors can disrupt the normal flow of execution, expose sensitive information, and lead to poor user experience. Hence, we need to implement a robust error-handling mechanim in FasAPI applications.
In this article, we will discuss the different types of errors in FastAPI to help you understand their causes and effects. We will also discuss the different ways to implement error handling in FastAPI using in-built methods and custom exception classes. Finally we will discuss some FastAPI error handling best practices to help you build robust APIs.

## What are errors and exceptions in FastAPI?

Errors and exectpions in FastAPI are situations where the normal flow of an application is interrupted due to an unexpected event, such as invalid input, missing data, or a failed database connection. For example, trying to divide a number by zero causes an error as it is not a valid mathematical operation.

FastAPI provides a structured way to handle errors using different exception handling mechanisms. After encountering an error, the FastAPI app raises an exception that disrupts the normal execution flow of the app. We can catch the exception, log the error messages, and send a meaningful response to the user.

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
After starting the FastAPI server, you can perform different operations by sending HTTP requests to the server. For example, you can send a POST request to the `/calculate` endpoint to add two numbers, as shown below:

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

Now that we have implemented the basic calculator app, let's discuss the differnt FastAPI errors.

## Different types of errors in FastAPI

Errors in FastAPI are caregorized into various types such as internal server error, validation error, and HTTP exception. Let's discss the different types of errors in FastAPI so that we can implement mechanisms to handle each of them.

### Internal Server Error

Internal server errors are caused by unexpected runtime issues like logical errors, math errors, or database issues that aren't explicitely handled by the program. For example, if the calculator app running on the FastAPI server tries to divide a number by zero, it will return internal server error due to ZeroDivisionError, as shown in the following example:

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
In this API call, we have passed zero as the second operand. Hence, the server returns `Internal Server Error` as its output:

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

The `Method Not Allowed` error occurs due to wrong HTTP method in the API call. If a FastAPI endpoint is defined using the POST request method and we call the API endpoint using GET request method, the FastAPI server runs into StarletteHTTPException with status code 405. For instance, we have defined the `/calculate` endpoint using the POST request method. When we send a GET request to the endpoint, the FastAPI app runs into StarletteHTTPException exception. 

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

FastAPI validates inputs using pydantic models. If an incoming request for a FastAPI endpoint doesn't conform to the declared structure and parameter types, FastAPI returns request validation error in response. For example, we have defined the /calculate endpoint with three inputs where the `operation` must be a string and `num1` and `num2` must be floating point numbers or values that can be converted to floats. When we pass a string that cannot be converted to a floating point number, we run into the request validation error.


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

HTTP exceptions are built-in FastAPI exceptions that we can use to raise exceptions and send error responses with standard HTTP status codes. When we raise an HTTP exception, FastAPI automatially handles the exception and returns the content in the `detail` parameter as the API response. For instance, we have raised an HTTP exception in our FastAPI app when the requested operation in the API call is other than add, subtract, multiply, and divide. Hence, if we pass `write` as an input to the operation field, the calculator app raises the HTTP exception.

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

### Custom exceptions in FastAPI

We can define custom FastAPI exceptions for handling errors by inheriting built-in Python exception classes. In the custom exception, we can define any number of attributes to store the information about the error. After defining the exception, we can create exception handlers to handle the custom exception. 

For example, we can create a custom `InvalidOperationError` exception by inheriting the Python `Exception` class to handle errors due to unsupported `operation` in the API requests to the calculator app. 

```
# Define a custom exception class
class InvalidOperationError(Exception):
    def __init__(self, message: str="Not a valid operation.",type: str= "FAILURE", code: int = 404):
        self.message = message
        self.code = code
        self.type=type
        super().__init__(message)
```

Next, we can create an exception handler using the `@app.exception_handler` decorator to handle the `InvalidOperationError` by raising an HTTPException to get the output for the API call.  

```
# Register an exception handler to handle the InvalidOperationError exception
@app.exception_handler(InvalidOperationError)
async def invalid_operation_exception_handler(request: Request,exc: InvalidOperationError):
    return JSONResponse(status_code=exc.code, content={"type":exc.type, "reason":exc.message})
```

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
{"type":"FAILURE","reason":"Not a valid operation."}
```
As you can see, the handler for the InvalidOperationError raises an HTTPException, which gives us the message output using the attributes of the InvalidOperationError. In the logs, FastAPI records this execution with `404 Not Found` message as we have assigned the 404 HTTP code to the InvalidOperationError.

```
INFO:     127.0.0.1:56798 - "POST /calculate/ HTTP/1.1" 404 Not Found
```
Now that we have discussed different FastAPI errors and custom exceptions, let's discuss how to handle FastAPI errors.

## How to handle errors and exceptions in FastAPI? 

We can use the try-except blocks to manually raise HTTPException with proper messages for different types of errors. We can also define custom exception handlers that handle exceptions of a particular type from the entire FastAPI app. Finally, we can create a global exception handler that handles any uncaughet exception, preventing the FastAPI exception from falling into an Internal Server Error. Let's discuss all the approces to handle FastAPI errors, starting with Python try-except blocks.

## Error handling using try-except in FastAPI

To handle errors using try-except blocks in a FastAPI application, we can manually handle different types of errors in the except blocks and raise HTTP exceptions with proper message and status code. For example, we can use the try-except blocks to handle errors caused during different operations in our FastAPI application as follows:

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
```

In this code, we have used try-except blocks to handle errors and raise HTTP exceptions for each operation. We also have the custom exception class with handler for the unsupported operations. Now, let's try to divide a number by zero using the /calculate API call.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```

The above API call triggers a ZeroDivisionError exception, which is handled by the except block of the divide operation, and we get the following output in the API response.

```json
{"detail":{"type":"FAILURE","reason":"Not able to divide 10.0 by 0.0."}}
```

In the logs, the above API call is recorded with the message `400 Bad Request` as we have set the status code to 400 while raising the HTTP exception.

```py
INFO:     127.0.0.1:52422 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```

A single exception can occur at multiple places in a program. Also, we might miss putting all the exception types in the except block of the code, which may lead to uncaught errors. 

We can use custom exception handlers to reduce code repetition and handle errors of a prticular type at one place, regardless of where they originate in the code. Custom exception handles also allow us to format errors of a specific type to follow a standard JSON format. Let's discuss how to handle FastAPI errors using custom exception handlers. 

## Error handling using custom exception handlers in FastAPI

FastAPI allows us to write custom handlers for each exception by defining functions using the `exception_handler` decorator. Each custom exception handler takes a Python Request and an Exception object as its input. Inside the exception handler, we can process the exception, log the error messages, and raise HTTPException with a proper message to return the API response. Once we have defined a custom exception handler, all the exceptions of the specified exception type are handled by the exception handler. 

For instance, we can define a custom exception handler to handle all the TypeError exceptions as follows:

```
@app.exception_handler(TypeError)
async def typeerror_handler(request: Request, exc: TypeError):
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"TypeError exception occurred due to mismatch between the expected and the actual data type of the operands."})
```

This exception handler will process all the TypeError exceptions irrespective of where they are raised in the FastAPI app. In a similar manner, we can define custom exception handlers for ZeroDivisionError and ValueError exceptions, as shown below:

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
    return JSONResponse(status_code=exc.code, content={"type":exc.type, "reason":exc.message})

# Register an exception handler to handle the TypeError exception
@app.exception_handler(TypeError)
async def typeerror_handler(request: Request, exc: TypeError):
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"TypeError exception occurred due to mismatch between the expected and the actual data type of the operands."})

# Register an exception handler to handle the ZeroDivisionError exception
@app.exception_handler(ZeroDivisionError)
async def zerodivisionerror_handler(request: Request,exc: ZeroDivisionError):
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Cannot perform division as the second operand is zero."})

# Register an exception handler to handle the ValueError exception
@app.exception_handler(ValueError)
async def valueerror_handler(request: Request,exc: ValueError):
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"ValueError exception occurred due to operands with correct data types but inappropriate values."})

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
Now, let's try to divide a number by zero using the /calculate API call.

```bash
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":10, "num2": 0}'
```
The FastAPI app returns an output as follows:

```json
{"type":"FAILURE","reason":"Cannot perform division as the second operand is zero."}
```
As you can see, the API response contains the message from the custom exception handler `zerodivisionerror_handler`. As we have defined the status code to 400 in the `zerodivisionerror_handler`, the log message also records the API call with the `400 Bad Request` message.

```py
INFO:     127.0.0.1:50036 - "POST /calculate/ HTTP/1.1" 400 Bad Request
```

Similarly, let's pass values to the API call that can cause the ValueError exception: 

```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1":1e308, "num2": 1e-100}'
```
In the above API call, we have passed `1e308` and `1e-100` as operands for the divide operation. As the division causes ValueError exception due to overflow, we get the following response from the custom exception handler defined for ValueError exceptions.

```
{"type":"FAILURE","reason":"ValueError exception occurred due to operands with correct data types but inappropriate values."}
```

FastAPI also allows us to access data from the API request in the in exception handlers. To do this, we can attach the input data received in the API request to the payload of the Request object. Then, we can access data in the exception handler using the payload attribute of the Request.state object. 

To do this, we will first define a dependency function `attach_payload` as follows:

1. The `attach_payload` function takes the payload of the API request and a Request object as its input.
2. Inside the `attach_payload` function, we will assign the payload of the API request to the state.payload parameter of the Request object.
3. After execution the attach_payload function returns the original payload of the API request.

The attach_payload function looks as follows:

```py
async def attach_payload(payload: InputData, request: Request = None):
    request.state.payload = payload
    return payload
```

After defining the attach_payload function, we will add it as a dependency to the calculation function of the /calculate API endpoint using the Depends function, as shown below:

```
@app.post("/calculate/")
async def calculation(input_data: InputData = Depends(attach_payload)):
    # function logic
```

After adding the dependency, FastAPI automatically executes the attach_payload function with the same input given to the calculation function. The attach_payload function then assigns the payload of the API request to the state.payload parameter of the Request object and returns the payload, which is then used by the calculate function to execute business logic. 

Now, the Request object has all the inputs passed in the API call in its state.payload attribute. Hence, we can access the inputs in the exception handlers through the Request object, log them, or send specific messages in the response to the API call based on the input values. 

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
    return JSONResponse(status_code=exc.code, content={"type":exc.type, "reason":exc.message, "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the TypeError exception
@app.exception_handler(TypeError)
async def typeerror_handler(request: Request,exc: TypeError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"TypeError exception occurred due to mismatch between the expected and the actual data type of the operands.", "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the ZeroDivisionError exception
@app.exception_handler(ZeroDivisionError)
async def zerodivisionerror_handler(request: Request,exc: ZeroDivisionError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Cannot perform division as the second operand is zero.", "operand_1":num1, "operand_2":num2, "operation":operation})

# Register an exception handler to handle the ValueError exception
@app.exception_handler(ValueError)
async def zerodivisionerror_handler(request: Request,exc: ValueError):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"ValueError exception occurred due to operands with correct data types but inappropriate values.", "operand_1":num1, "operand_2":num2, "operation":operation})

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
In this code, we have used a dependency function to attach payload to the Request object and used the Request object to get the inputs to the API endpoint. The exception handlers also return the input along with the reason whenever an error occurs. Now, let's send an API request with unsupported operation to the FastAPI app:

```
curl http://127.0.0.1:8080/calculate/ -X POST -H "Content-Type: application/json" -d '{"operation": "write", "num1":10, "num2": 10}'
```
The above request raises InvalidOperationError, which is then handled by the exception handler and we get the following output:

```
{"type":"FAILURE","reason":"Not a valid operation.","operand_1":10.0,"operand_2":10.0,"operation":"write"}
```

As you can see, the exception handler is able to access the inputs passed in the API call.

Custom exception handlers are a great way to handle FastAPI errors of specific type. However, it is almost impossible to define and handle every type of error using custom exception handlers. To catch and handle any uncaught exception, we can use global exception handlers. 

## Using a global exception handler in FastAPI

A global exception handler in FastAPI handles exceptions of type `Exception`, which is the base class for any Python exception. We can create a global exception handler using the `exception_handler` decorator as follows:

```py
@app.exception_handler(Exception)
async def global_exception_handler(request: Request,exc: Exception):
    payload = getattr(request.state, "payload", None)
    num1 = payload.num1
    num2 = payload.num2
    operation=payload.operation
    return JSONResponse(status_code=500, content={"type":"FAILURE", "reason":"An unexpected error occurred.", "operand_1":num1, "operand_2":num2, "operation":operation})
```

The above exception handler can handle any FastAPI error that isn't handled by any other exception handler. This makes sure that the FastAPI app doesn't run into Internal Server Error after any exception. 

Now that we have discussed the different types of FastAPI errors and handling them, let's discuss some best practices for handling errors in FastAPI.

## FastAPI error handling best practices

### Use HTTPException to raise exceptions

HTTPException helps us raise exceptions with specific status code and error messages. Also, HTTPException is automatically handled by FastAPI and the content passed to the `detail` parameter of the HTTPException construcor is returned as the API response. Hence, you should use the HTTPException class to raise exceptions with proper status codes and message. 

```
if operation not in ["add", "subtract", "multiply", "divide"]:
        raise HTTPException(status_code=404, detail={"type":"FAILURE", "reason":"Not a valid operation"})
```

### Use JSONResponse in exception handlers 

You should avoid raising HTTPException inside exception handlers as it causes nested exception. While handling errors through a custom exception handler, always use the JSONResponse class to return API responses with suitable status codes. 

```
@app.exception_handler(ZeroDivisionError)
async def zerodivisionerror_handler(request: Request,exc: ZeroDivisionError):
    return JSONResponse(status_code=400, content={"type":"FAILURE", "reason":"Cannot perform division as the second operand is zero."})
```

### Create Custom Exception Classes for Domain and Business Logic Errors

You should use custom exception classes for domain errors instead of raising generic exceptions. This will help you handle errors, log error-specific messages, and send proper responses to the users.

For instance, the calculator app supports only addition, subtraction, multiplication, and division. Hence, we have defined a custom exception class named `InvalidOperationError` to raise exceptions for unsupported operations. 

```
class InvalidOperationError(Exception):
    def __init__(self, message: str="Not a valid operation.",type: str= "FAILURE", code: int = 404):
        self.message = message
        self.code = code
        self.type=type
        super().__init__(message)
```

After defining custom exception classes, you can register and exception handler to handle them.For instance, we have implemented the exception handler for the InvalidOperationError exception as follows:

```
@app.exception_handler(InvalidOperationError)
async def invalid_operation_exception_handler(request: Request,exc: InvalidOperationError):
    return JSONResponse(status_code=exc.code, content={"type":exc.type, "reason":exc.message})
```
In a similar manner, you can write custom exception classes for domain and business logic errors, and write exception handlers to handle the custom exceptions.

### Implement a Global Exception Handler

Always implement a global exception handler that handles any uncaught exception and returns a safe response instead of crashing the server. To do this, you can build an exception handler for Python Exception class as follows:

```
@app.exception_handler(Exception)
async def global_exception_handler(request: Request,exc: Exception):
    return JSONResponse(status_code=500, content={"type":"FAILURE", "reason":"An unexpected error occurred."})
```

The global exception handler handles any uncaught FastAPI error and prevents the server from crashing due to errors.

### Standardize Error Response Format

It is important to standardize the error response format. This makes is easier for the frontend developers to parse the error response and show proper error messages to the user. For example, we have defined the error response format with fields type, reason, operand_1, operand_2, and operation.

```
{"type":"FAILURE", "reason":"Error message", "operand_1":num1, "operand_2":num2, "operation":operation}
```

All the exception handlers in our app return the error messages in the same format, which will make parsing the error messages easier.

### Customize Validation Error Responses

Every validation error response has a different structure. For example, if we send an API request with correct number of fields but incorrect data types, we get the following validation error response

```
{"detail":[{"type":"json_invalid","loc":["body",43],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting value"}}]}
```

On the other hand, if we send an API request with a missing field, we get the following response:

```
{"detail":[{"type":"missing","loc":["body","num2"],"msg":"Field required","input":{"operation":"divide","num1":10}}]}
```

To standardize these responses, you can write an exception handler as follows:

```
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request,exc: RequestValidationError):
    error=exc.errors()
    return JSONResponse(status_code=422, content={"type":"RequestValidationError", "error_type":error[0]["type"], "reason":error[0]["msg"]})
```
After implementing this exception handler, we get the following response for the API request with incorrect values:

```
{"type":"RequestValidationError","error_type":"json_invalid","reason":"JSON decode error"}
```
For the API request with missing values, we get the following response:
```
{"type":"RequestValidationError","error_type":"missing","reason":"Field required"}
```
As you can see, both the responses have the same structure and they can be processed by the frontend app to show appropriate error messages to the user. Hence, it is important to handle request validation errors explicitely and standardize their responses.

### Use logging and email alerts for observability

It is important to log the error messages and exception trace before sending the error response. The error logs can help identify root cause of the errors and debug them to build a robust application. You should also configure email alerts for critical issues like security breaches, rate limit errors, or out of memory errors that should not be ignored.

### Map Internal Errors to Safe Public Messages

You should never reveal internal Python error messages to users in the error response. Doing so can expose user credentials, API keys, and PII that shouldn't be accessible outside the system. Hence, Always write exception handlers that map internal Python errors to safe public messages free of credentials and PIIs.

## Conclusion
This section will summarize what the article discussed and include a CTA.

## Frequently asked questions

### 1. What is error 404 not found in FastAPI?
In FastAPI, the "404 Not Found" error indicates that the URL path or endpoint we are trying to access through the API request does not correspond to any defined endpoint in the FastAPI application. 

### 2. What is 422 unprocessable entity in FastAPI?
In FastAPI, the "422 Unprocessable Entity" error indicates that the server understands the content type and syntax of payload in the request, but it cannot process the request due to semantic errors in the request body, such as missing required fields, incorrect data types, invalid data format, or mismatch in parameter handling. 

### 3. Should I return 204 or 404?
You should return 404 if the requested resource or endpoint doesn't exist. On the other hand, 204 should be used when the request is processed successfully but there is no content to return in the response body. 

### 4. Should HTTP delete return 200 or 204?
You should use the "204 No Content" status for successful delete operations if you don't need to send back any information to the client in response. However, if you want to return information like confirmation message or details about the deleted resource, you should use the "200 OK" status. 

### 5. How to avoid cors error in FastAPI?
To avoid cross origin resource sharing (CORS) errors in FastAPI, you can use CORSMiddleware in your FastAPI application to allow cross origin requests.

```
from fastapi.middleware.cors import CORSMiddleware

# Define a list of origins that are allowed to make cross origin requests. 
origins = ["http://localhost.honeybadger.io", "https://localhost.honeybadger.io", "http://localhost", "http://localhost:8080"]

# Add middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins, # Use ["*"] to allow all the origins 
    allow_methods = ["*"] # List of allowed HTTP methods. Defaults to ["GET"]. ["*"] allows all the methods.
    allow_headers = ["*"] # List of HTTP request headers supported for cross origin requests. Defaults to []. ["*"] allows all the headers.
)
```

I hope you enjoyed reading the article. Happy Learning!
