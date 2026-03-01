import functools
import time


def log_execution_time(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_log_execution_time(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value

    return wrapper_log_execution_time


def login_required(func):
    """User autentication check"""

    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        instance = args[0]
        if not getattr(instance, "user_logined", False):
            raise PermissionError("Error: User must be logged in")
        return func(*args, **kwargs)

    return wrapper_login_required
