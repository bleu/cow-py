import backoff
import httpx
from cow_py.common.config import CowEnv, SupportedChainId

DEFAULT_BACKOFF_OPTIONS = {
    "max_tries": 10,
    "max_time": None,
    "jitter": None,
}

DEFAULT_LIMITER_OPTIONS = {"rate": 5, "per": 1.0}

ORDER_BOOK_PROD_CONFIG = {
    SupportedChainId.MAINNET: "https://api.cow.fi/mainnet",
    SupportedChainId.GNOSIS_CHAIN: "https://api.cow.fi/xdai",
    SupportedChainId.SEPOLIA: "https://api.cow.fi/sepolia",
}

ORDER_BOOK_STAGING_CONFIG = {
    SupportedChainId.MAINNET: "https://barn.api.cow.fi/mainnet",
    SupportedChainId.GNOSIS_CHAIN: "https://barn.api.cow.fi/xdai",
    SupportedChainId.SEPOLIA: "https://barn.api.cow.fi/sepolia",
}


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
    async def make_request(self, client, url, method, **request_kwargs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        return await client.request(
            url=url, headers=headers, method=method, **request_kwargs
        )


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


class ResponseAdapter:
    async def adapt_response(self, response):
        raise NotImplementedError()


class RequestBuilder:
    def __init__(self, strategy, response_adapter):
        self.strategy = strategy
        self.response_adapter = response_adapter

    async def execute(self, client, url, method, **kwargs):
        response = await self.strategy.make_request(client, url, method, **kwargs)
        return await self.response_adapter.adapt_response(response)


class JsonResponseAdapter(ResponseAdapter):
    async def adapt_response(self, response):
        if response.headers.get("content-type") == "application/json":
            return await response.json()
        else:
            return response.text
