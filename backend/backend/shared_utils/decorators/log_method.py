import logging
from typing import Any, Callable, TypeVar
from functools import wraps
import time

# Type variable for generic function types
F = TypeVar('F', bound=Callable[..., Any])

# Get the logger for the current module
logger = logging.getLogger(__name__)

def log_method(func: F) -> F:
    """
    A decorator that logs method entry, exit, and any exceptions raised.

    This decorator will log:
    - When the method is entered, including the method name and arguments.
    - When the method exits, including the method name and execution time.
    - Any exceptions raised during method execution.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function.

    Raises:
        Exception: Re-raises any exception caught during the function execution.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        try:
            logger.debug(f"Entering {func_name} - Args: {args}, Kwargs: {kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"Exiting {func_name} - Execution time: {execution_time:.2f} seconds")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func_name}: {str(e)}")
            raise
    return wrapper

# Example usage
@log_method
def example_function(x: int, y: int) -> int:
    """
    An example function to demonstrate the log_method decorator.

    Args:
        x (int): First integer.
        y (int): Second integer.

    Returns:
        int: The sum of x and y.

    Raises:
        ValueError: If either x or y is negative.
    """
    if x < 0 or y < 0:
        raise ValueError("Both arguments must be non-negative")
    return x + y

if __name__ == "__main__":
    result = example_function(5, 3)
    print(f"Result: {result}")

    try:
        example_function(-1, 3)
    except ValueError:
        pass  # Exception will be logged by the decorator