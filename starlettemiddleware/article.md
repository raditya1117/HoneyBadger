## What is a middleware in web applications?

A middleware in a web application is a software component that sits in between the request or response and the application endpoint. 

- When a web app receives a request, a middleware intercepts the request, inspects it, and modifies it if required before passing the request to the application endpoint ot next middleware.
- When an endpoint returns a response, a middleware again intercepts the response, inspects it, and modifies it if required before the application sends back the response. 

You can think of middlewares as a pipeline of software components to implement functionalities that apply globally across the web application rather than in individual endpoints. Without middlewares, we would repeat a logic in every endpoint if it needs to be applied to every request and response. Middlewares apply functionalities such as authentication, logging, and monitoring to the requests and responses from every endpoint in the web application. 

## What is a Starlette Middleware?

Starlette middleware is an intermediate processing layer between the client request and application endpoint. Starlette middlewares intercept incoming HTTP requests to the starlette app before they reach the route handler and process the outgoing responses before they are returned to the client. Given that Starlette is an Asynchronous Server Gateway Interface (ASGI) framework, starlette middlewares also support asynchronous request handling. 

### Defining starlette middlewares

We can define starlette middlewares using two approaches. We can either define a pure ASGI middleware using the core parameters of the application or we can use the BaseHTTPMiddleware class to define a high-level middleware.

#### Pure ASGI middleware
An ASGI application has core parameters like scope, receive, and send that define how the web servers like Uvicorn and the Python web applications communicate. 

- The scope parameter contains a dictionary that has metadata such as request type, HTTP method, URL path, query parameters, protocol details, headers, client information, and server information for a connection or request.
- The receive parameter contains a callable function used to receive events or messages from the client. The web applications calls the receive function when it wants more data.
- The send parameter contains a callable function used to send events or messages back to the client.

 We can use these parameters to build pure ASGI middlewares for a starlette application, as shown below:

```py
pure asgi starlette middleware
```
Instead of using the scope, receive, and send parameters to define a middleware, we can use the BaseHTTPMiddleware class defined in the starlette.middleware.base module to create starlette middlewares for HTTP connections.

#### BaseHTTPMiddleware
BaseHTTPMiddleware helps us create starlette middlewares using a simple request/response interface instead of handling the low-level ASGI messages. To create a middleware using BaseHTTPMiddleware, we just need to inherit the BaseHTTPMiddleware class and implement a dispatch() method to process requets and responses, as shown below:

```py
BaseHTTPMiddleware example
```

Both the approaches to create starlette middlewares has it own advantages and disadvantages. For instance, Middlewares created using BaseHTTPMiddleware only process requests with scope type 'http'. They do not work on websocket connections. However,BaseHTTPMiddleware is sufficient for tasks like logging, authentication, rate limiting, and request-ID injection. 

On the contrary, pure ASGI middlewares are useful for applications that must intercept websocket traffic, preserve streaming, share contextvars, or operae in high-throughput environments. For example, streaming tasks where the web application returns chunks over time. 

Now that we have a basic understanding of what middlewares are and what they do, let's discuss some starlette middleware examples. 

## Starlette middleware examples

### CORSMiddleware

### SessionMiddleware

### HTTPSRedirectMiddleware

### TrustedHostMiddleware

### GZipMiddleware

### Custom starlette middleware examples

## How to add a middleware in a starlette application?

### Using add_middleware()

### Passing middleware to starlette constructor

## How to add a starlette middleware in a FastAPI application? 

### Using add_middleware()

### Using FastAPI's @app.middleware("http") Decorator

### Using starlette middleware in FastAPI's Constructor

## Using multiple starlette midllewares in an application

### Starlette middleware execution order

### Example using multiple starlette middlewares in a FastAPI application
