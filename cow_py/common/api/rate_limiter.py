from aiolimiter import AsyncLimiter

DEFAULT_LIMITER_OPTIONS = {"rate": 5, "per": 1.0}


def rate_limitted(
    rate=DEFAULT_LIMITER_OPTIONS["rate"], per=DEFAULT_LIMITER_OPTIONS["per"]
):
    limiter = AsyncLimiter(rate, per)

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with limiter:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
