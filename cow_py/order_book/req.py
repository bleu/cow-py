import httpx

from cow_py.common.config import CowEnv, SupportedChainId
from cow_py.order_book.api_config import (
    APIConfigFactory,
    GetRequestStrategy,
    PostRequestStrategy,
    backoff_decorator,
    rate_limit_decorator,
)
from cow_py.order_book.generated.model import Address, Trade
from cow_py.order_book.requests import DEFAULT_BACKOFF_OPTIONS, DEFAULT_LIMITER_OPTIONS


class ResponseAdapter:
    async def adapt_response(self, response):
        raise NotImplementedError()


class JsonResponseAdapter(ResponseAdapter):
    async def adapt_response(self, response):
        if response.headers.get("content-type") == "application/json":
            return await response.json()
        else:
            return response.text


class RequestBuilder:
    def __init__(self, strategy, response_adapter):
        self.strategy = strategy
        self.response_adapter = response_adapter

    async def execute(self, client, url, **kwargs):
        response = await self.strategy.make_request(client, url, **kwargs)
        return await self.response_adapter.adapt_response(response)


Context = dict[str, str]


class OrderBookApi:
    def __init__(self, context: Context = {}):
        self.config = APIConfigFactory.get_config(
            context.get("env", CowEnv.PROD),
            context.get("chain_id", SupportedChainId.MAINNET),
        )

    @backoff_decorator(DEFAULT_BACKOFF_OPTIONS)
    @rate_limit_decorator(DEFAULT_LIMITER_OPTIONS)
    async def _fetch(self, path, method, context_override: Context = {}, **kwargs):
        context = {**self.config.get_context(), **context_override}
        url = context.get("base_url") + path
        async with httpx.AsyncClient() as client:
            builder = RequestBuilder(
                GetRequestStrategy() if method == "GET" else PostRequestStrategy(),
                JsonResponseAdapter(),
            )
            return await builder.execute(client, url, **kwargs)

    async def get_version(self, context_override: Context = {}):
        return await self._fetch("/api/v1/version", "GET", context_override)

    async def get_trades_by_owner(self, owner: Address, context_override: Context = {}):
        response = await self._fetch(
            "/api/v1/trades", "GET", context_override, params={"owner": owner}
        )
        return [Trade(**trade) for trade in response]
