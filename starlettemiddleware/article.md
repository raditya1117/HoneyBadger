## What is a middleware in web applications?

A middleware in a web application is a software component that sits in between the request or response and the application endpoint. 

- When a web app receives a request, a middleware intercepts the request, inspects it, and modifies it if required before passing the request to the application endpoint ot next middleware.
- When an endpoint returns a response, a middleware again intercepts the response, inspects it, and modifies it if required before the application sends back the response. 

You can think of middlewares as a pipeline of software components to implement functionalities that apply globally across the web application rather than in individual endpoints. Without middlewares, we would repeat a logic in every endpoint if it needs to be applied to every request and response. Middlewares apply functionalities such as authentication, logging, and monitoring to the requests and responses from every endpoint in the web application. 
