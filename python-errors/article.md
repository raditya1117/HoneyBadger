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
