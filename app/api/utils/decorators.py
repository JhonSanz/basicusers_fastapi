from typing import Callable, TypeVar, List
from functools import wraps
from pydantic import ValidationError

T = TypeVar("T")


def validate_res_model_pydantic(model_class: T):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, list):
                try:
                    result = [model_class.model_validate(item) for item in result]
                except ValidationError as e:
                    print(e)
                    raise Exception(f"Validation error: {e}")
            else:
                try:
                    result = model_class.model_validate(result)
                except ValidationError as e:
                    print(e)
                    raise Exception(f"Validation error: {e}")
            return result

        return wrapper

    return decorator
