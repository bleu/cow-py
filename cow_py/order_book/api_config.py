import backoff
import httpx
from cow_py.order_book import ORDER_BOOK_PROD_CONFIG, ORDER_BOOK_STAGING_CONFIG
from cow_py.common.config import CowEnv


class APIConfig:
    def __init__(self, chain_id):
        self.chain_id = chain_id

    def get_base_url(self):
        raise NotImplementedError()


class ProdAPIConfig(APIConfig):
    def get_context(self):
        return {
            "base_url": ORDER_BOOK_PROD_CONFIG.get(
                self.chain_id, "default URL if chain_id is not found"
            ),
        }


class StagingAPIConfig(APIConfig):
    def get_context(self):
        return {
            "base_url": ORDER_BOOK_STAGING_CONFIG.get(
                self.chain_id, "default URL if chain_id is not found"
            ),
        }


# Modify the APIConfigFactory to accept chain_id
class APIConfigFactory:
    @staticmethod
    def get_config(env, chain_id):
        if env == CowEnv.PROD:
            return ProdAPIConfig(chain_id)
        elif env == CowEnv.STAGING:
            return StagingAPIConfig(chain_id)
        else:
            raise ValueError("Unknown environment")


class RequestStrategy:
    async def make_request(self, client, url, **kwargs):
        raise NotImplementedError()


class GetRequestStrategy(RequestStrategy):
    async def make_request(self, client, url, **kwargs):
        return await client.get(url, **kwargs)


class PostRequestStrategy(RequestStrategy):
    async def make_request(self, client, url, **kwargs):
        return await client.post(url, **kwargs)


def backoff_decorator(backoff_opts):
    def decorator(func):
        @backoff.on_exception(backoff.expo, httpx.HTTPStatusError, **backoff_opts)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def rate_limit_decorator(limiter_opts):
    # TODO: Implement rate limit decorator
    def decorator(func):
        return func

    return decorator
