# Decorators

A **decorator** in **Python** is any callable **Python** object that is used to modify a function or a class. This assignment is about implementing various simple decorators to accomplish tiny features in our functions.

## Allows a function to run only on odd seconds

A simple decorator to make the function return the output only if the current time has seconds numeric as an odd digit.

```python
def odd_it(fn: "Function"):
    """
    Decorator that lets a function run only when the 'second' numeric
    in current tinme is odd.
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        CURR_TIME = datetime.now()
        print(CURR_TIME)
        if CURR_TIME.second % 2 != 0:
            return fn(*args, **kwargs)
    return inner
```

## Logs

A decorator to print the logs of a function, the start time of execution, end time, running time. Also, whether the function returns something, it's docs. The decorator adds these functionality for us.

```python
def log_it(fn: "Function"):
    """
    Decorator to add the log printing functionality to
    a function.
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        run_dt = datetime.now()
        result = fn(*args, **kwargs)
        end_dt = datetime.now()
        print(f"{run_dt}: called {fn.__name__}")
        print(f"Execution time: {end_dt - run_dt}")
        print(f"Function description:\n{fn.__doc__}")
        print(f"Function returned something: {True if result else False}")
        return result
    return inner
```

## Authenticate

Decorator to implement simple authentication functionality and give that to any function of our choice. The user can make use of a closure to provide the current password. It has to match with the default user password provided beforehand.

```python
def set_password() -> "Function":
    """
    A simple closure to set and store a permanent pssword.
    """
    password = ""

    def inner():
        nonlocal password
        if password == "":
            password = get_password()
        return password

    return inner


def authenticate(curr_password: str, user_password: str):
    """
    Wrapper used to authenticate the function before executing the function.
    curr_password: `set_password` closure to get password from user.
    :param user_password: pre-defined password compared with the `curr_password`.
    """ 

    def decor(fn: "Function"):
        @wraps(fn)
        def inner(*args, **kwargs):
            if user_password == curr_password():
                print("You are authenticated")
                return fn(*args, **kwargs)
            else:
                print("Wrong Password!!!")

        return inner

    return decor
```

## Average time

A decorator factory, that takes in an integer, defining the number of iteration of which a function's runtime has to be calculated and average is calculated. It returns a decorator.

```python
def time_it(reps: int):
    """
    Decorator factory to take in an integer defining the number of
    iterations and return a decorator accordingly.
    """
    if type(reps) is not int:
        raise TypeError("Invalid type, expected int!")
    if reps < 1:
        raise ValueError("Hey! Let it time for atleast 1 iteration.")
    def timed(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            total_elapsed = 0
            for i in range(reps):
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                total_elapsed += (end - start)
            avg_run_time = total_elapsed / reps
            print('Avg Run time: {0:.6f}s ({1} reps)'.format(avg_run_time, reps))
            return result
        return inner
    return timed
```

## Privilege

Decorator that provides privilege access. A function can have four parameters and based on the privileges (high, mid, low, no), access is given to all 4, 3, 2 or 1 parameters.

```python
class Privilege:
    """
    This decorator class  wraps any function with certain privileges which
    limits the arguments passed to the function. Based on privileges (high, mid, low, no),
    it provides access to all 4, 3, 2 or 1 parameters.
    """

    def __init__(self, privilege="no"):
        if privilege and privilege in ("high", "mid", "low", "no"):
            self.privilege = privilege
        else:
            self.privilege = "no"

    def __call__(self, fn):

        @wraps(fn)
        def inner(base, **kwargs):
            params = list(kwargs.items())
            cnt = {"high": 3, "mid": 2, "low": 1, "no":0}
            if len(params) < cnt[self.privilege] :
                raise ValueError("Invalid number of keyword arguments!")

            if self.privilege == "high":
                return fn(base, **dict(params[:3]))

            elif self.privilege == "mid":
                return fn(base, **dict(params[:2]))

            elif self.privilege == "low":
                return fn(base, **dict(params[:1]))

            elif self.privilege == "no":
                return fn(base)
        return inner
```

## Single dispatch

Writing HTMLize code using `singledispatch`, available as a built-in decorator in `functools` module. Also the idea is to add functionality using monkey patching and not make every thing hard coded.

```python
@singledispatch
def htmlize(str_esc: str) -> str:
    """
    Converts the newline character in a string to contain a br tag.
    input: string to escape.
    return: string, transformed
    """
    return escape(str(str_esc)).replace("\n", "<br/>\n")
```

After this, functions to handle other types are added one by one, available in the code.

## Test Case Performance

![](result.png)