from typing import List, Dict, Any

from cow_py.common.chains import Chain

from eth_account import Account

from eth_account.messages import encode_structured_data

from eth_utils.crypto import keccak

from cow_py.contracts.order import Order

from cow_py.order_signing.types import SigningResult
from cow_py.order_signing.utils import (
    sign_order,
    sign_order_cancellation,
    sign_order_cancellations,
    get_domain,
)


class OrderSigningUtils:
    @staticmethod
    def sign_order(order: Order, chain: Chain, signer: Account) -> SigningResult:
        return sign_order(order, chain, signer)

    @staticmethod
    def sign_order_cancellation(
        order_uid: str, chain: Chain, signer: Account
    ) -> SigningResult:
        return sign_order_cancellation(order_uid, chain, signer)

    @staticmethod
    def sign_order_cancellations(
        order_uids: List[str], chain: Chain, signer: Account
    ) -> SigningResult:
        return sign_order_cancellations(order_uids, chain, signer)

    @staticmethod
    def get_domain(chain: Chain) -> Dict[str, Any]:
        return get_domain(chain)

    @staticmethod
    def get_domain_separator(chain: Chain) -> str:
        domain = OrderSigningUtils.get_domain(chain)
        hash = encode_structured_data(domain)
        return keccak(hash.body).hex()

    @staticmethod
    def get_eip712_types() -> Dict[str, List[Dict[str, str]]]:
        return {
            "Order": [
                {"name": "sellToken", "type": "address"},
                {"name": "buyToken", "type": "address"},
                {"name": "receiver", "type": "address"},
                {"name": "sellAmount", "type": "uint256"},
                {"name": "buyAmount", "type": "uint256"},
                {"name": "validTo", "type": "uint32"},
                {"name": "appData", "type": "bytes32"},
                {"name": "feeAmount", "type": "uint256"},
                {"name": "kind", "type": "string"},
                {"name": "partiallyFillable", "type": "bool"},
                {"name": "sellTokenBalance", "type": "string"},
                {"name": "buyTokenBalance", "type": "string"},
            ]
        }
