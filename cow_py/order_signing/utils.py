from dataclasses import asdict
from typing import Dict, List, Union, Callable, Any

from eth_account.account import Account


from cow_py.common.chains import Chain
from cow_py.contracts.domain import TypedDataDomain, domain as domain_gp
from cow_py.contracts.order import Order
from cow_py.contracts.sign import Signature, SigningScheme
from cow_py.order_book.generated.model import EcdsaSigningScheme
from cow_py.order_signing.types import (
    SigningResult,
    SignOrderParams,
    SignOrderCancellationParams,
    SignOrderCancellationsParams,
)

from cow_py.contracts.sign import (
    sign_order as sign_order_gp,
    sign_order_cancellation as sign_order_cancellation_gp,
    sign_order_cancellations as sign_order_cancellations_gp,
)
from cow_py.common.constants import COW_PROTOCOL_SETTLEMENT_CONTRACT_CHAIN_ADDRESS_MAP
from cow_py.common.cow_error import CowError


MAP_SIGNING_SCHEMA = {
    EcdsaSigningScheme.eip712: SigningScheme.EIP712,
    EcdsaSigningScheme.ethsign: SigningScheme.ETHSIGN,
}

PayloadParams = Union[
    SignOrderParams,
    SignOrderCancellationParams,
    SignOrderCancellationsParams,
]


def _sign_order(params: SignOrderParams) -> Signature:
    chain = params.chainId
    account = params.signer
    order = params.order
    signing_scheme = params.signingScheme

    domain = get_domain(chain)

    return sign_order_gp(domain, order, account, MAP_SIGNING_SCHEMA[signing_scheme])


def _sign_order_cancellation(params: SignOrderCancellationParams) -> Signature:
    chain = params.chainId
    account = params.signer
    signing_scheme = params.signingScheme
    order_uid = params.orderUid

    domain = get_domain(chain)

    return sign_order_cancellation_gp(
        domain, order_uid, account, MAP_SIGNING_SCHEMA[signing_scheme]
    )


def _sign_order_cancellations(params: SignOrderCancellationsParams) -> Signature:
    chain = params.chainId
    account = params.signer
    signing_scheme = params.signingScheme
    order_uids = params.orderUids

    domain = get_domain(chain)

    return sign_order_cancellations_gp(
        domain, order_uids, account, MAP_SIGNING_SCHEMA[signing_scheme]
    )


def _sign_payload(
    payload: PayloadParams,
    sign_fn: Callable[[Dict[str, Any]], Signature],
    account: Account,
    signing_scheme: EcdsaSigningScheme = EcdsaSigningScheme.eip712,
) -> SigningResult:
    signature = sign_fn(
        {**asdict(payload), "account": account, "signingScheme": signing_scheme}
    )
    data = signature.data if signature else None

    return SigningResult(
        signature=str(data) if data else "", signingScheme=signing_scheme
    )


def sign_order(
    order: Order,
    chain: Chain,
    account: Account,
) -> SigningResult:
    """
    Returns the signature for the specified order with the signing scheme encoded
    into the signature.
    :param order: The order to sign.
    :param chain: The chain ID.
    :param account: The account used to sign the order.
    :return: Encoded signature including signing scheme for the order.
    """
    return _sign_payload(
        {"order": order, "chainId": chain.chain_id}, _sign_order, account
    )


def sign_order_cancellation(
    order_uid: str,
    chain: Chain,
    account: Account,
) -> SigningResult:
    """
    Returns the signature for the Order Cancellation with the signing scheme encoded
    into the signature.
    :param order_uid: The unique identifier of the order being cancelled.
    :param chain: The chain ID.
    :param account: The account used to sign the order cancellation.
    :return: Encoded signature including signing scheme for the order.
    """
    return _sign_payload(
        {"orderUid": order_uid, "chainId": chain.chain_id},
        _sign_order_cancellation,
        account,
    )


def sign_order_cancellations(
    order_uids: List[str],
    chain: Chain,
    account: Account,
) -> SigningResult:
    """
    Returns the signature for the Order Cancellations with the signing scheme encoded
    into the signature.
    :param order_uids: The unique identifiers of the orders being cancelled.
    :param chain: The CoW Protocol protocol `chainId` context that's being used.
    :param account: The account used to sign the order cancellations.
    :return: Encoded signature including signing scheme for the order.
    """
    return _sign_payload(
        {"orderUids": order_uids, "chainId": chain.chain_id},
        _sign_order_cancellations,
        account,
    )


def get_domain(chain: Chain) -> TypedDataDomain:
    """
    Returns the TypedDataDomain used for signing for the specified chainId.
    :param chain: The chain ID.
    :return: The TypedDataDomain for the specified chainId.
    :raises CowError: If the chainId is not supported.
    """
    # Get settlement contract address
    settlement_contract = COW_PROTOCOL_SETTLEMENT_CONTRACT_CHAIN_ADDRESS_MAP.get(
        chain.chain_id
    )

    if not settlement_contract:
        raise CowError("Unsupported network. Settlement contract is not deployed")

    return domain_gp(chain, settlement_contract)
