import hashlib
import json
from functools import wraps

from db.session import r


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        status = "on"
        if status == "on":
            cache_key = hashlib.sha256(str(sorted(kwargs["query_params"])).encode("utf-8")).hexdigest()
            cache_result = r.get(cache_key)

            if cache_result is not None:
                print("from key")
                return json.loads(cache_result)
            else:
                result = func(*args, **kwargs)
                response, status_code = result
                if status_code < 400:
                    r.setex(cache_key, 60, json.dumps(response))
            return result

        elif status == "off":
            result = func(*args, **kwargs)
            return result

    return wrapper
