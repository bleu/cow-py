from typing import Any, Optional

import httpx

from cow_py.common.api.backoff import with_backoff
from cow_py.common.api.rate_limiter import rate_limitted

Context = dict[str, Any]


class APIConfig:
    def __init__(self, chain_id, base_context: Optional[Context]):
        self.chain_id = chain_id
        self.context = base_context or {}

    def get_base_url(self):
        raise NotImplementedError()

    def get_context(self):
        return self.context


class RequestStrategy:
    async def make_request(self, client, url, method, **request_kwargs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        return await client.request(
            url=url, headers=headers, method=method, **request_kwargs
        )


class ResponseAdapter:
    async def adapt_response(self, _response):
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


class WithConfig:
    @staticmethod
    def get_config(context: Context):
        raise NotImplementedError()


class ApiBase:
    def __init__(self, context: Context = {}):
        self.config = self.__class__.get_config(
            context,
        )

    @staticmethod
    def get_config(context: Context):
        raise NotImplementedError()

    def _with_context(self, context: Context):
        return self.__class__({**self.config.get_context(), **context})

    @with_backoff()
    @rate_limitted()
    async def _fetch(self, path, method="GET", **kwargs):
        url = self.config.get_base_url() + path
        print("TRIED TO FETCH")

        del kwargs["context_override"]

        async with httpx.AsyncClient() as client:
            builder = RequestBuilder(
                RequestStrategy(),
                JsonResponseAdapter(),
            )
            return await builder.execute(client, url, method, **kwargs)
