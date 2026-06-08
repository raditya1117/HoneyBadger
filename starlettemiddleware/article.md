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
Browsers enforce same-origin policy. A page loaded from one network endpoint(IP and port pair) isn't allowed to make fetch requests to another network endpoint, unles the server explicitely permits it. CORSMiddleware handles this issue by intercepting every incoming request and attaching appropriate access control response headers. We can define a CORSMiddleware in starlette as follows:

```
CORSMiddleware example
```

In the above middleware definition

- The allow_origins parameter takes a list of origin strings permitted to make cross-origin requests. To allow cross-origin requests for all the origins, you can pass a list `['*']` as input to the allow_origins parameter.
- The allow_credentials parameter, when set to True, permits the browser to include cookies and Authorization headers in cross-origin requests. The allow_credentials parameter cannot be set to True when  allow_origins is set to `['*']`.
-  The allow_methods parameters takes a list of methods the browser is allowed to use in cross-origin requests. By default, it is set to `["GET"]`.
 -  The allow_headers parameter defines the request headers the browser is allowed to include. The allowed values include Accept, Accept-Language, Content-Language, and Content-Type among others. 
-  The expose_headers parameter defines the response headers the browser is allowed to read from cross-origin responses via Javascript. By default, browsers only expose a set of safe headers like 'Cache-Control', 'Content-Language', 'Content-Type', 'Expires', 'Last-Modified', and 'Pragma'.
-  The max_age parameter defines the maximum time in seconds the browser can cache a preflight response. It defaults to 600 seconds.


### SessionMiddleware
The session middleware adds server-managed and cookie-based session support to the web application. When we enable a SessionMiddleware, a request.session dictionary becomes available in every route handler. At the end of each request, Starlette serializes the session dictionary to JSON, signs it with a secret key, encodes the result, and writes it to a cookie. On the next request, the middleware reads the cookie, verifies the signature, and deserializes the payload back into request.session. 

```
Session  middleware example.
```

In the above middleware definition,

- The secret_parameter takes the HMAC signing key as its input. Rotating the key invalidates every existing session and logs out all the active users. 
-  The session_cookie parameter takes the name of the cookie written to the client. It defaults to "session".
-  The max_age parameter defines the cookie lifetime in seconds, with a default value of 14 days.
-  The same_site parameter controls when the browser sends the cookie in cross-site contexts. When set to the default value "lax", the browser sends the cookie on top-level negotiations bit nopt on cross-site sub-requests. When set to "strict", the browser never sends the cookie cross-site. When we set the same_site parameter to "none", the browser always sends the cookient but it requires https_only parameter to be set to True.
-  The https_only parameter sets the cookie's `Secure` flag. When set to True, it restricts the cookie transmission to HTTPS connections. 


The session data lives in the cookie, which is signed but not encrypted. Hence, we shouldn't store any secrets in the request.session object. Also, the cookie sizes are limited to 4096 bytes. Hence, we should use it only for state variables like user ID, a CSRF token, preference flag, and OAuth state parameter. 



### HTTPSRedirectMiddleware
The HTTPSRedirectMiddleware ensures that all the traffic reaches the web application over and encrypted connection. It inspects the `scope['scheme']` attribute of every incoming request and responds with a `307 Temporary Redirect` to the equivalent `https` or `wss` URL for every `HTTP` or `ws` request. We can define a HTTPSRedirectMiddleware as follows: 

```py
HTTPSRedirectMiddleware example
```
The HTTPSRedirectMiddleware takes no configuration parameter. It redirects every plaintext request and lets the encrypted requets pass through unchanged. In terms of position, the HTTPSRedirectMiddleware should stay in the outermost layers, just inside TrustedHostMiddleware as there is no value in running authentication or session logic on a connection that is about to be redirected. 

### TrustedHostMiddleware

The TrustedHostMiddleware guards the web application against HTTP host header injection attacks. TrustedHostMiddleware reads the Host header from every incoming request and compares it against an allowed list of hosts. Requests with a host not present on the allowed list received 400 Bad Request and never proceed further. 

```
trusted host example
```
- The allowed_hosts parameter exact hostnames or `*` prefixed wildcard patterns. The hostname matching is performed on exact values by default, while the subdomnains are supported via the `*` prefix. If you pass a list with single `*` i.e. `["*"]` to the allowed_hosts parameter, it allows all the hosts, effectively disabling the protection provided by TrustedHostMiddleware.
- The www_redirect parameter redirects the requests from host myapp.com to www.myapp.com if only the www.myapp.com is present in the allowed_hosts list.

The TrustedHostMiddleware should reside at the outermost layer of the middleware stack so that invalid hosts are rejected before any other layer processes the request. 


### GZipMiddleware
The GZipMiddleware compresses the response body using the GZip algorithn whenever the client advertises support via `Accept-Encoding: gzip`. Compressing the response reduces bytes transmitted over the network, which lowers latency and bandwidth costs. It reduces the size of JSON responses by 70-90% and HMTL responses by 60-80%. We can define the GZipMiddleware as follows:

```
gzip middleware code
```

In this code, 

- The minimum_size parameter defines the lower limit of response size in Bytes to be Gzipped. Response bodies smaller than `minimum_size` bytes aren't compressed.
- The compresslevel parameter control the speed and ratio of compression. Level 1 compresses the response quickly while level 9 compresess more aggressively and takes time. For most API rsponses, level 6 provides the right balance between compression and time. 

The GZipMiddleware processes the response after the route handler runs. If the client supports GZip encoding and the response body exceeds minimum_size, the middleware replaces the response body with a compressed version and adds `Content-Encoding: gzip` to the response headers. It also adds `Vary: Accept-Encoding` to the header so that caching proxies store separate compressed and uncompressed copies keyed by the client's `Accept-Encoding`. Responses smaller than minimum_size are passed untouched. 

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
