# Errors in Python
Errors in Python are abnormal conditions that interrupt the normal program execution. In this article, we will discuss the different types of errors and exceptions in Python. We will also discuss how you can avoid Python errors effectively. 


## What are the different types of errors in Python?
We can broadly categorize Python errors into four types.

1. Syntax errors: Syntax errors occur due to invalid syntax, incorrect indentation, or typos.
2. Runtime errors:Runtime errors occur during program execution when the Python interpreter encounters an invalid operation.
3. Logical errors: Logical errors are caused due to error in the logic of the program when the code runs without error but produces incorrect results.
4. File and I/O errors: These errors occur during file operations or input/output tasks.
5. System level errors: System level errors are raised by the Python runtime environment or the operating system due to reasons like memory overflow or interruptions.

Let's discuss all these errors one-by-one in detail, starting with syntax errors.

## Syntax Errors in Python

As the name suggests, syntax errors are the errors caused by invalid syntax or code structure. Syntax errors are often caused due to typos or incorrect indentation. Common syntax errors include indentation errors, unclosed strings and brackets. 

```
if x > 10
    print("HoneyBadger")
```
output:

```
File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1
    if x > 10
             ^
SyntaxError: expected ':'
```
```
```
### Indentation error

```
if x > 10:
print("HoneyBadger")
```
output
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2
    print("HoneyBadger")
    ^
IndentationError: expected an indented block after 'if' statement on line 1
```

another

```
def say_hello(name):
print(f"Hi {name}, you are at HoneyBadger")
    
```
output
```
File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2
    print(f"Hi {name}, you are at HoneyBadger")
    ^
IndentationError: expected an indented block after function definition on line 1
```
```
def say_hello(name):
  print(f"Hi {name}, you are at HoneyBadger")
 print("Great seeing you here.")
```
output

```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 3
    print("Great seeing you here.")
                                   ^
IndentationError: unindent does not match any outer indentation level
```
### Unclosed strings/ brackets
similarly

```
if x > 10:
    print("HoneyBadger)
```
output:
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2
    print("HoneyBadger)
          ^
SyntaxError: unterminated string literal (detected at line 2)
```
bracjets
```
print("HoneyBadger"
```
output
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1
    print("HoneyBadger"
         ^
SyntaxError: '(' was never closed
```
similarly

```
my_list=[1,2,3
```
output
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1
    my_list=[1,2,3
            ^
SyntaxError: '[' was never closed

```
Ymight run into this issue while using nested function calls, if else conditions or using pandas 

### TabError

```
def say_hello(name):
	print(f"Hi {name}, you are at HoneyBadger") # Indentation using Tab
    print("Great seeing you here.")  # Indentation using four spaces

```
output:
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 3
    print("Great seeing you here.") # Indentation using four spaces
TabError: inconsistent use of tabs and spaces in indentation

```
Python 3 explicitly disallows mixing tabs and spaces for indentation in a way that makes the meaning ambiguous.
### Invalid assignment errors

```
"name"="HoneyBadger"
```
output
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1
    "name"="HoneyBadger"
    ^^^^^^
SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='?
```

alternate
```
class="HoneyBadger"
```
output
```
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1
    class="HoneyBadger"
         ^
SyntaxError: invalid syntax
```

## Runtime errors

### Arithmetic errors 

```
x = 10 / 0
```
output

```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    x = 10 / 0
ZeroDivisionError: division by zero

```
### NameError
```
print(HoneyBadger)
```
output
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    print(HoneyBadger)
NameError: name 'HoneyBadger' is not defined

```
### UnboundLocalError
scope error
```
def say_hello():
	print(greeting)
	greeting="Hi, you are at HoneyBadger"

say_hello()
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 5, in <module>
    say_hello()
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2, in say_hello
    print(greeting)
UnboundLocalError: local variable 'greeting' referenced before assignment
```
### TypeError
```
x=10+"HoneyBadger"
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    x=10+"HoneyBadger"
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

### ValueError
correct type inappropriate value
```
x=10+int("HoneyBadger")
```

output:

```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    x=10+int("HoneyBadger")
ValueError: invalid literal for int() with base 10: 'HoneyBadger'
```

### Index and Key errors

```
my_list=[1,2,3,4,5,6]
print(my_list[6])
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2, in <module>
    print(my_list[6])
IndexError: list index out of range
```
keyerror
```
my_dict={"a":1,"b":2,"c":3,"d":4}
print(my_dict["e"])
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2, in <module>
    print(my_dict["e"])
KeyError: 'e'
```
### Modulenotfounderrorv -- import error
```
import honeybadger
print("You are at HoneyBadger")
```
output
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    import honeybadger
ModuleNotFoundError: No module named 'honeybadger'
```
ModuleNotFoundError is a subclass of ImportError, raised specifically when the interpreter cannot locate the module file itself. ImportError is a broader, more general exception that can be raised for various other issues during the import process, even if the module file is found.

### AttributeError

```
my_list=5
my_list.append(6)
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 2, in <module>
    my_list.append(6)
AttributeError: 'int' object has no attribute 'append'
```

### RecursionError
Occurs when recursion depth exceeds limit. Happens becuase we forget to add a base case or terminating condition
```
def increment_till_hundred(x):
	x+=1
	print(x)
	increment_till_hundred(x)
increment_till_hundred(80)
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 5, in <module>
    increment_till_hundred(80)
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 4, in increment_till_hundred
    increment_till_hundred(x)
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 4, in increment_till_hundred
    increment_till_hundred(x)
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 4, in increment_till_hundred
    increment_till_hundred(x)
  [Previous line repeated 992 more times]
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 3, in increment_till_hundred
    print(x)
RecursionError: maximum recursion depth exceeded while calling a Python object
```
```
def increment_till_hundred(x):
	x+=1
	print(x)
	if x<100:
		increment_till_hundred(x)
increment_till_hundred(80)
```

When a file cannot be opened it is an IOError but the IOError is a subset of and OSError. This change was made in Python 3.3. It is not a Runtime error. I emailed the author of my textbook and he was kind enough to reply and confirm. 

## System-level errors in Python
OSError

```
file=open("nonexistentfile.txt","r")
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    file=open("nonexistentfile.txt","r")
FileNotFoundError: [Errno 2] No such file or directory: 'nonexistentfile.txt'
```

permission error

```
file=open("samplefile.txt","a")
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    file=open("samplefile.txt","a")
PermissionError: [Errno 13] Permission denied: 'samplefile.txt'
```
alt
```
file=open("/home/aditya1117/codes/HoneyBadger/python-errors","r")
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    file=open("/home/aditya1117/codes/HoneyBadger/python-errors","r")
IsADirectoryError: [Errno 21] Is a directory: '/home/aditya1117/codes/HoneyBadger/python-errors'
```
### MemoryError

```
my_list=[10] * (10**10)
```
output:

```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    my_list=[10] * (10**10)
MemoryError
```

### KeyboardInterrupt

```
while True:
	pass
```
output:
```
^CTraceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 1, in <module>
    while True:
KeyboardInterrupt

```
### Connecction error

```
import requests
response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 4, in <module>
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
  File "/home/aditya1117/.local/lib/python3.10/site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
  File "/home/aditya1117/.local/lib/python3.10/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/aditya1117/.local/lib/python3.10/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/aditya1117/.local/lib/python3.10/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "/home/aditya1117/.local/lib/python3.10/site-packages/requests/adapters.py", line 700, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='jsonplaceholder.typicode.com', port=443): Max retries exceeded with url: /todos/1 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7400d45a6c80>: Failed to resolve 'jsonplaceholder.typicode.com' ([Errno -3] Temporary failure in name resolution)"))
```

### Connection refused error

```
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))
```
output:
```
Traceback (most recent call last):
  File "/home/aditya1117/codes/HoneyBadger/python-errors/code.py", line 3, in <module>
    s.connect(("localhost", 9999))
ConnectionRefusedError: [Errno 111] Connection refused
```
