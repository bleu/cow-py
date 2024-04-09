import unittest
from cow_py.order_book.generated.model import (
    UID,
    OrderQuoteResponse,
    Trade,
    OrderQuoteRequest,
)
import httpx
from unittest.mock import AsyncMock, patch
from cow_py.order_book import (
    OrderBookApi,
    OrderCreation,
)


class TestOrderBookApi(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api = OrderBookApi()

    async def asyncTearDown(self):
        pass

    async def test_get_version(self):
        expected_version = "1.0.0"
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = httpx.Response(200, text=expected_version)
            version = await self.api.get_version()
            mock_request.assert_called_once()
            self.assertEqual(version, expected_version)

    async def test_get_trades_by_order_uid(self):
        mock_trade_data = {
            "blockNumber": 123456,
            "logIndex": 789,
            "orderUid": "mock_order_uid",
            "owner": "mock_owner_address",
            "sellToken": "mock_sell_token_address",
            "buyToken": "mock_buy_token_address",
            "sellAmount": "100",
            "sellAmountBeforeFees": "120",
            "buyAmount": "200",
            "txHash": "mock_transaction_hash",
        }

        mock_trade = Trade(**mock_trade_data)
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = httpx.Response(200, json=[mock_trade_data])
            trades = await self.api.get_trades_by_order_uid("mock_order_uid")
            mock_request.assert_called_once()
            self.assertEqual(trades, [mock_trade])

    async def test_post_quote(self):
        mock_order_quote_request_data = {
            "sellToken": "0x",
            "buyToken": "0x",
            "receiver": "0x",
            "appData": "app_data_object",
            "appDataHash": "0x",
            "from": "0x",
            "priceQuality": "verified",
            "signingScheme": "eip712",
            "onchainOrder": False,
        }
        mock_order_quote_request = OrderQuoteRequest(**mock_order_quote_request_data)
        mock_order_quote_response_data = {
            "quote": {
                "sellToken": "0x",
                "buyToken": "0x",
                "receiver": "0x",
                "sellAmount": "0",
                "buyAmount": "0",
                "feeAmount": "0",
                "validTo": 0,
                "appData": "0x",
                "partiallyFillable": True,
                "sellTokenBalance": "erc20",
                "buyTokenBalance": "erc20",
                "kind": "buy",
            },
            "verified": True,
            "from": "0x",
            "expiration": "0",
        }

        mock_order_quote_response = OrderQuoteResponse(**mock_order_quote_response_data)
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = httpx.Response(
                200, json=mock_order_quote_response_data
            )
            response = await self.api.post_quote(mock_order_quote_request)
            mock_request.assert_called_once()
            self.assertEqual(response, mock_order_quote_response)

    async def test_post_order(self):
        mock_response = "mock_uid"
        mock_order_creation = OrderCreation(
            sellToken="0x",
            buyToken="0x",
            sellAmount="0",
            buyAmount="0",
            validTo=0,
            feeAmount="0",
            kind="buy",
            partiallyFillable=True,
            appData="0x",
            signingScheme="eip712",
            signature="0x",
        )
        with patch.object(self.api, "_fetch", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_response
            response = await self.api.post_order(mock_order_creation)
            mock_fetch.assert_called_once()
            self.assertEqual(response, UID(mock_response))
