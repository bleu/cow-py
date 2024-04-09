from dataclasses import dataclass
from typing import Any, Dict
import backoff
import httpx


class OrderBookApiError(Exception):
    def __init__(self, response: httpx.Response, body: Any):
        self.response = response
        self.body = body
        message = str(body) if isinstance(body, str) else response.reason_phrase
        super().__init__(message)


REQUEST_TIMEOUT = 408
TOO_EARLY = 425
TOO_MANY_REQUESTS = 429
INTERNAL_SERVER_ERROR = 500
BAD_GATEWAY = 502
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504

STATUS_CODES_TO_RETRY = [
    REQUEST_TIMEOUT,
    TOO_EARLY,
    TOO_MANY_REQUESTS,
    INTERNAL_SERVER_ERROR,
    BAD_GATEWAY,
    SERVICE_UNAVAILABLE,
    GATEWAY_TIMEOUT,
]

DEFAULT_BACKOFF_OPTIONS = {
    "max_tries": 10,
    "max_time": None,
    "jitter": None,
}

DEFAULT_LIMITER_OPTIONS = {"rate": 5, "per": 1.0}


@dataclass
class FetchParams:
    path: str
    method: str


async def get_response_body(response: httpx.Response) -> Any:
    if response.status_code != 204:
        try:
            if "application/json" in response.headers.get("content-type", ""):
                return response.json()
            else:
                return response.text
        except Exception as e:
            print(e)
    return None


async def request(
    base_url: str,
    path: str,
    method: str = "GET",
    backoff_opts: Dict[str, Any] = None,
    **request_kwargs,
) -> Any:

    @backoff.on_exception(backoff.expo, httpx.HTTPStatusError, **backoff_opts)
    async def make_request():
        async with httpx.AsyncClient() as client:
            url = f"{base_url}{path}"
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
            }
            response = await client.request(
                url=url, headers=headers, method=method, **request_kwargs
            )
            response_body = await get_response_body(response)

            if 200 <= response.status_code < 300:
                return response_body

            raise OrderBookApiError(response, response_body)

    return await make_request()
