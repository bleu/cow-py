from typing import List, Any

from dataclasses import dataclass
from cow_py.order_book.generated.model import EcdsaSigningScheme
from cow_py.common.chains import Chain


from cow_py.contracts.order import Order


@dataclass
class SigningResult:
    """
    Encoded signature including signing scheme for the order.
    """

    signature: str
    signingScheme: EcdsaSigningScheme


@dataclass
class SignOrderParams:
    """
    Parameters for signing an order intent.
    """

    chainId: Chain
    signer: Any  # Replace Any with the actual type of Signer
    order: Order
    signingScheme: EcdsaSigningScheme


@dataclass
class SignOrderCancellationParams:
    """
    Parameters for signing an order cancellation.
    """

    chainId: Chain
    signer: Any  # Replace Any with the actual type of Signer
    orderUid: str
    signingScheme: EcdsaSigningScheme


@dataclass
class SignOrderCancellationsParams:
    """
    Parameters for signing multiple bulk order cancellations.
    """

    chainId: Chain
    signer: Any  # Replace Any with the actual type of Signer
    orderUids: List[str]
    signingScheme: EcdsaSigningScheme
