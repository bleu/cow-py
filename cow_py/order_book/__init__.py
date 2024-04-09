from dataclasses import asdict
from typing import Any, Dict, List
from cow_py.common.config import DEFAULT_COW_API_CONTEXT, CowEnv, SupportedChainId
from cow_py.order_book.requests import DEFAULT_BACKOFF_OPTIONS, request
from .generated.model import (
    AppDataObject,
    Trade,
    Order,
    TotalSurplus,
    NativePriceResponse,
    SolverCompetitionResponse,
    OrderQuoteRequest,
    OrderQuoteResponse,
    OrderCreation,
    UID,
    Address,
    TransactionHash,
    AppDataHash,
    OrderCancellation,
)

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


class OrderBookApi:
    def __init__(self, context: Dict[str, Any] = None):
        if context is None:
            context = {}
        self.context = {
            **asdict(DEFAULT_COW_API_CONTEXT),
            "backoffOpts": DEFAULT_BACKOFF_OPTIONS,
            **context,
        }

    def get_api_url(self, context: Dict[str, Any]) -> str:
        if context.get("env", CowEnv.PROD) == CowEnv.PROD:
            return ORDER_BOOK_PROD_CONFIG[
                context.get("chain_id", SupportedChainId.MAINNET)
            ]
        return ORDER_BOOK_STAGING_CONFIG[
            context.get("chain_id", SupportedChainId.MAINNET)
        ]

    async def _fetch(
        self,
        path: str,
        params: Dict[str, Any] = None,
        context_override: Dict[str, Any] = None,
    ) -> Any:
        context = self._get_context_with_override(context_override)
        url = self.get_api_url(context)
        backoff_opts = context.get("backoffOpts", DEFAULT_BACKOFF_OPTIONS)
        return await request(url, path=path, params=params, backoff_opts=backoff_opts)

    def _get_context_with_override(
        self, context_override: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        if context_override is None:
            context_override = {}
        return {**self.context, **context_override}

    async def get_version(self, context_override: Dict[str, Any] = None) -> str:
        return await self._fetch(
            path="/api/v1/version", context_override=context_override
        )

    async def get_trades_by_owner(
        self, owner: Address, context_override: Dict[str, Any] = None
    ) -> List[Trade]:
        response = await self._fetch(
            path="/api/v1/trades",
            params={"owner": owner},
            context_override=context_override,
        )
        return [Trade(**trade) for trade in response]

    async def get_trades_by_order_uid(
        self, order_uid: UID, context_override: Dict[str, Any] = None
    ) -> List[Trade]:
        response = await self._fetch(
            path="/api/v1/trades",
            params={"order_uid": order_uid},
            context_override=context_override,
        )
        return [Trade(**trade) for trade in response]

    async def get_orders_by_owner(
        self,
        owner: Address,
        limit: int = 1000,
        offset: int = 0,
        context_override: Dict[str, Any] = None,
    ) -> List[Order]:
        return [
            Order(**order)
            for order in await self._fetch(
                path=f"/api/v1/account/{owner}/orders",
                params={"limit": limit, "offset": offset},
                context_override=context_override,
            )
        ]

    async def get_order_by_uid(
        self, order_uid: UID, context_override: Dict[str, Any] = None
    ) -> Order:
        response = await self._fetch(
            path=f"/api/v1/orders/{order_uid}",
            context_override=context_override,
        )
        return Order(**response)

    def get_order_link(
        self, order_uid: UID, context_override: Dict[str, Any] = None
    ) -> str:
        return (
            self.get_api_url(self._get_context_with_override(context_override))
            + f"/orders/{order_uid}"
        )

    async def get_tx_orders(
        self, tx_hash: TransactionHash, context_override: Dict[str, Any] = None
    ) -> List[Order]:
        response = await self._fetch(
            path=f"/api/v1/transactions/{tx_hash}/orders",
            context_override=context_override,
        )
        return [Order(**order) for order in response]

    async def get_native_price(
        self, tokenAddress: Address, context_override: Dict[str, Any] = None
    ) -> NativePriceResponse:
        response = await self._fetch(
            path=f"/api/v1/token/{tokenAddress}/native_price",
            context_override=context_override,
        )
        return NativePriceResponse(**response)

    async def get_total_surplus(
        self, user: Address, context_override: Dict[str, Any] = None
    ) -> TotalSurplus:
        response = await self._fetch(
            path=f"/api/v1/users/{user}/total_surplus",
            context_override=context_override,
        )
        return TotalSurplus(**response)

    async def get_app_data(
        self, app_data_hash: AppDataHash, context_override: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        return await self._fetch(
            path=f"/api/v1/app_data/{app_data_hash}",
            context_override=context_override,
        )

    async def get_solver_competition(
        self, action_id: int = "latest", context_override: Dict[str, Any] = None
    ) -> SolverCompetitionResponse:
        response = await self._fetch(
            path=f"/api/v1/solver_competition/{action_id}",
            context_override=context_override,
        )
        return SolverCompetitionResponse(**response)

    async def get_solver_competition_by_tx_hash(
        self, tx_hash: TransactionHash, context_override: Dict[str, Any] = None
    ) -> SolverCompetitionResponse:
        response = await self._fetch(
            path=f"/api/v1/solver_competition/by_tx_hash/{tx_hash}",
            context_override=context_override,
        )
        return SolverCompetitionResponse(**response)

    async def get_quote(
        self, request: OrderQuoteRequest, context_override: Dict[str, Any] = None
    ) -> OrderQuoteResponse:
        response = await self._fetch(
            path=f"/api/v1/quote",
            json=asdict(request),
            context_override=context_override,
        )
        return OrderQuoteResponse(**response)

    async def post_quote(
        self, request: OrderQuoteRequest, context_override: Dict[str, Any] = None
    ) -> OrderQuoteResponse:
        response = await self._fetch(
            path=f"/api/v1/quote",
            json=asdict(request),
            context_override=context_override,
            method="POST",
        )
        return OrderQuoteResponse(**response)

    async def post_order(order: OrderCreation, context_override: Dict[str, Any] = None):
        response = await self._fetch(
            path="/api/v1/orders",
            json=asdict(order),
            context_override=context_override,
            method="POST",
        )
        return UID(response)

    async def delete_order(
        orders_cancelation: OrderCancellation, context_override: Dict[str, Any] = None
    ):
        response = await self._fetch(
            path=f"/api/v1/orders",
            json=asdict(orders_cancelation),
            context_override=context_override,
            method="DELETE",
        )
        return UID(response)

    async def put_app_data(
        self,
        app_data: AppDataObject,
        app_data_hash: str = None,
        context_override: Dict[str, Any] = None,
    ) -> AppDataHash:
        app_data_hash_url = app_data_hash if app_data_hash else ""
        response = await self._fetch(
            path=f"/api/v1/app_data/{app_data_hash_url}",
            json=app_data,
            context_override=context_override,
            method="PUT",
        )
        return AppDataHash(response)
