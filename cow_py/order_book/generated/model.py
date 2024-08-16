# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/cowprotocol/services/v2.245.1/crates/orderbook/openapi.yml
#   timestamp: 2024-04-12T14:44:16+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, RootModel


class TransactionHash(RootModel[str]):
    root: str = Field(
        ...,
        description="32 byte digest encoded as a hex with `0x` prefix.",
        examples=["0xd51f28edffcaaa76be4a22f6375ad289272c037f3cc072345676e88d92ced8b5"],
    )


class Address(RootModel[str]):
    root: str = Field(
        ...,
        description="20 byte Ethereum address encoded as a hex with `0x` prefix.",
        examples=["0x6810e776880c02933d47db1b9fc05908e5386b96"],
    )


class AppData(RootModel[str]):
    root: str = Field(
        ...,
        description="The string encoding of a JSON object representing some `appData`. The\nformat of the JSON expected in the `appData` field is defined\n[here](https://github.com/cowprotocol/app-data).\n",
        examples=['{"version":"0.9.0","metadata":{}}'],
    )


class AppDataHash(RootModel[str]):
    root: str = Field(
        ...,
        description="32 bytes encoded as hex with `0x` prefix.\nIt's expected to be the hash of the stringified JSON object representing the `appData`.\n",
        examples=["0x0000000000000000000000000000000000000000000000000000000000000000"],
    )


class AppDataObject(BaseModel):
    fullAppData: Optional[AppData] = None


class BigUint(RootModel[str]):
    root: str = Field(
        ...,
        description="A big unsigned integer encoded in decimal.",
        examples=["1234567890"],
    )


class CallData(RootModel[str]):
    root: str = Field(
        ...,
        description="Some `calldata` sent to a contract in a transaction encoded as a hex with `0x` prefix.",
        examples=["0xca11da7a"],
    )


class TokenAmount(RootModel[str]):
    root: str = Field(
        ...,
        description="Amount of a token. `uint256` encoded in decimal.",
        examples=["1234567890"],
    )


class PlacementError(Enum):
    QuoteNotFound = "QuoteNotFound"
    ValidToTooFarInFuture = "ValidToTooFarInFuture"
    PreValidationError = "PreValidationError"


class OnchainOrderData(BaseModel):
    sender: Address = Field(
        ...,
        description="If orders are placed as on-chain orders, the owner of the order might\nbe a smart contract, but not the user placing the order. The\nactual user will be provided in this field.\n",
    )
    placementError: Optional[PlacementError] = Field(
        None,
        description="Describes the error, if the order placement was not successful. This could\nhappen, for example, if the `validTo` is too high, or no valid quote was\nfound or generated.\n",
    )


class EthflowData(BaseModel):
    refundTxHash: TransactionHash = Field(
        ...,
        description="Specifies in which transaction the order was refunded. If\nthis field is null the order was not yet refunded.\n",
    )
    userValidTo: int = Field(
        ...,
        description="Describes the `validTo` of an order ethflow order.\n\n**NOTE**: For ethflow orders, the `validTo` encoded in the smart\ncontract is `type(uint256).max`.\n",
    )


class OrderKind(Enum):
    buy = "buy"
    sell = "sell"


class OrderClass(Enum):
    market = "market"
    limit = "limit"
    liquidity = "liquidity"


class SellTokenSource(Enum):
    erc20 = "erc20"
    internal = "internal"
    external = "external"


class BuyTokenDestination(Enum):
    erc20 = "erc20"
    internal = "internal"


class PriceQuality(Enum):
    fast = "fast"
    optimal = "optimal"
    verified = "verified"


class OrderStatus(Enum):
    presignaturePending = "presignaturePending"
    open = "open"
    fulfilled = "fulfilled"
    cancelled = "cancelled"
    expired = "expired"


class ProtocolAppData(BaseModel):
    pass


class AuctionPrices(RootModel[Optional[Dict[str, BigUint]]]):
    root: Optional[Dict[str, BigUint]] = None


class UID(RootModel[str]):
    root: str = Field(
        ...,
        description="Unique identifier for the order: 56 bytes encoded as hex with `0x` prefix.\nBytes 0..32 are the order digest, bytes 30..52 the owner address and bytes\n52..56 the expiry (`validTo`) as a `uint32` unix epoch timestamp.\n",
        examples=[
            "0xff2e2e54d178997f173266817c1e9ed6fee1a1aae4b43971c53b543cffcc2969845c6f5599fbb25dbdd1b9b013daf85c03f3c63763e4bc4a"
        ],
    )


class SigningScheme(Enum):
    eip712 = "eip712"
    ethsign = "ethsign"
    presign = "presign"
    eip1271 = "eip1271"


class EcdsaSigningScheme(Enum):
    eip712 = "eip712"
    ethsign = "ethsign"


class EcdsaSignature(RootModel[str]):
    root: str = Field(
        ...,
        description="65 bytes encoded as hex with `0x` prefix. `r || s || v` from the spec.",
        examples=[
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        ],
    )


class PreSignature(RootModel[str]):
    root: str = Field(
        ...,
        description='Empty signature bytes. Used for "presign" signatures.',
        examples=["0x"],
    )


class ErrorType(Enum):
    DuplicatedOrder = "DuplicatedOrder"
    QuoteNotFound = "QuoteNotFound"
    InvalidQuote = "InvalidQuote"
    MissingFrom = "MissingFrom"
    WrongOwner = "WrongOwner"
    InvalidEip1271Signature = "InvalidEip1271Signature"
    InsufficientBalance = "InsufficientBalance"
    InsufficientAllowance = "InsufficientAllowance"
    InvalidSignature = "InvalidSignature"
    InsufficientFee = "InsufficientFee"
    SellAmountOverflow = "SellAmountOverflow"
    TransferSimulationFailed = "TransferSimulationFailed"
    ZeroAmount = "ZeroAmount"
    IncompatibleSigningScheme = "IncompatibleSigningScheme"
    TooManyLimitOrders_UnsupportedBuyTokenDestination = (
        "TooManyLimitOrders UnsupportedBuyTokenDestination"
    )
    UnsupportedSellTokenSource = "UnsupportedSellTokenSource"
    UnsupportedOrderType = "UnsupportedOrderType"
    InsufficientValidTo = "InsufficientValidTo"
    ExcessiveValidTo = "ExcessiveValidTo"
    InvalidNativeSellToken = "InvalidNativeSellToken"
    SameBuyAndSellToken = "SameBuyAndSellToken"
    UnsupportedToken = "UnsupportedToken"
    InvalidAppData = "InvalidAppData"
    AppDataHashMismatch = "AppDataHashMismatch"
    AppdataFromMismatch = "AppdataFromMismatch"


class OrderPostError(BaseModel):
    errorType: ErrorType
    description: str


class ErrorType1(Enum):
    InvalidSignature = "InvalidSignature"
    WrongOwner = "WrongOwner"
    OrderNotFound = "OrderNotFound"
    AlreadyCancelled = "AlreadyCancelled"
    OrderFullyExecuted = "OrderFullyExecuted"
    OrderExpired = "OrderExpired"
    OnChainOrder = "OnChainOrder"


class OrderCancellationError(BaseModel):
    errorType: ErrorType1
    description: str


class ErrorType2(Enum):
    AlreadyCancelled = "AlreadyCancelled"
    OrderFullyExecuted = "OrderFullyExecuted"
    OrderExpired = "OrderExpired"
    OnChainOrder = "OnChainOrder"
    DuplicatedOrder = "DuplicatedOrder"
    InsufficientFee = "InsufficientFee"
    InsufficientAllowance = "InsufficientAllowance"
    InsufficientBalance = "InsufficientBalance"
    InsufficientValidTo = "InsufficientValidTo"
    ExcessiveValidTo = "ExcessiveValidTo"
    InvalidSignature = "InvalidSignature"
    TransferSimulationFailed = "TransferSimulationFailed"
    UnsupportedToken = "UnsupportedToken"
    WrongOwner = "WrongOwner"
    SameBuyAndSellToken = "SameBuyAndSellToken"
    ZeroAmount = "ZeroAmount"
    UnsupportedBuyTokenDestination = "UnsupportedBuyTokenDestination"
    UnsupportedSellTokenSource = "UnsupportedSellTokenSource"
    UnsupportedOrderType = "UnsupportedOrderType"


class ReplaceOrderError(BaseModel):
    errorType: ErrorType2
    description: str


class ErrorType3(Enum):
    UnsupportedToken = "UnsupportedToken"
    ZeroAmount = "ZeroAmount"
    UnsupportedOrderType = "UnsupportedOrderType"


class PriceEstimationError(BaseModel):
    errorType: ErrorType3
    description: str


class OrderQuoteSideKindSell(Enum):
    sell = "sell"


class OrderQuoteSideKindBuy(Enum):
    buy = "buy"


class OrderQuoteValidity1(BaseModel):
    validTo: Optional[int] = Field(
        None, description="Unix timestamp (`uint32`) until which the order is valid."
    )


class OrderQuoteValidity2(BaseModel):
    validFor: Optional[int] = Field(
        None,
        description="Number (`uint32`) of seconds that the order should be valid for.",
    )


class OrderQuoteValidity(RootModel[Union[OrderQuoteValidity1, OrderQuoteValidity2]]):
    root: Union[OrderQuoteValidity1, OrderQuoteValidity2] = Field(
        ..., description="The validity for the order."
    )


class Objective(BaseModel):
    total: Optional[float] = Field(
        None, description="The total objective value used for ranking solutions."
    )
    surplus: Optional[float] = None
    fees: Optional[float] = None
    cost: Optional[float] = None
    gas: Optional[int] = None


class Order1(BaseModel):
    id: Optional[UID] = None
    executedAmount: Optional[BigUint] = None


class SolverSettlement(BaseModel):
    solver: Optional[str] = Field(None, description="Name of the solver.")
    solverAddress: Optional[str] = Field(
        None,
        description="The address used by the solver to execute the settlement on-chain.\nThis field is missing for old settlements, the zero address has been used instead.\n",
    )
    objective: Optional[Objective] = None
    score: Optional[BigUint] = Field(
        None,
        description="The score of the current auction as defined in [CIP-20](https://snapshot.org/#/cow.eth/proposal/0x2d3f9bd1ea72dca84b03e97dda3efc1f4a42a772c54bd2037e8b62e7d09a491f).\nIt is `null` for old auctions.\n",
    )
    clearingPrices: Optional[Dict[str, BigUint]] = Field(
        None,
        description="The prices of tokens for settled user orders as passed to the settlement contract.\n",
    )
    orders: Optional[List[Order1]] = Field(None, description="Touched orders.")
    callData: Optional[CallData] = Field(
        None,
        description="Transaction `calldata` that is executed on-chain if the settlement is executed.",
    )
    uninternalizedCallData: Optional[CallData] = Field(
        None,
        description="Full `calldata` as generated from the original solver output.\n\nIt can be different from the executed transaction if part of the settlements are internalised\n(use internal liquidity in lieu of trading against on-chain liquidity).\n\nThis field is omitted in case it coincides with `callData`.\n",
    )


class NativePriceResponse(BaseModel):
    price: Optional[float] = Field(None, description="Estimated price of the token.")


class TotalSurplus(BaseModel):
    totalSurplus: Optional[str] = Field(None, description="The total surplus.")


class InteractionData(BaseModel):
    target: Optional[Address] = None
    value: Optional[TokenAmount] = None
    call_data: Optional[List[CallData]] = Field(
        None, description="The call data to be used for the interaction."
    )


class Surplus(BaseModel):
    factor: float
    max_volume_factor: float


class Volume(BaseModel):
    factor: float


class FeePolicy(RootModel[Union[Surplus, Volume]]):
    root: Union[Surplus, Volume] = Field(
        ..., description="Defines the ways to calculate the protocol fee."
    )


class OrderParameters(BaseModel):
    sellToken: Address = Field(..., description="ERC-20 token to be sold.")
    buyToken: Address = Field(..., description="ERC-20 token to be bought.")
    receiver: Optional[Address] = Field(
        None,
        description="An optional Ethereum address to receive the proceeds of the trade instead\nof the owner (i.e. the order signer).\n",
    )
    sellAmount: TokenAmount = Field(
        ..., description="Amount of `sellToken` to be sold in atoms."
    )
    buyAmount: TokenAmount = Field(
        ..., description="Amount of `buyToken` to be bought in atoms."
    )
    validTo: int = Field(
        ..., description="Unix timestamp (`uint32`) until which the order is valid."
    )
    appData: AppDataHash
    feeAmount: TokenAmount = Field(
        ..., description="feeRatio * sellAmount + minimal_fee in atoms."
    )
    kind: OrderKind = Field(..., description="The kind is either a buy or sell order.")
    partiallyFillable: bool = Field(
        ..., description="Is the order fill-or-kill or partially fillable?"
    )
    sellTokenBalance: Optional[SellTokenSource] = "erc20"
    buyTokenBalance: Optional[BuyTokenDestination] = "erc20"
    signingScheme: Optional[SigningScheme] = "eip712"


class OrderMetaData(BaseModel):
    creationDate: str = Field(
        ...,
        description="Creation time of the order. Encoded as ISO 8601 UTC.",
        examples=["2020-12-03T18:35:18.814523Z"],
    )
    class_: OrderClass = Field(..., alias="class")
    owner: Address
    uid: UID
    availableBalance: Optional[TokenAmount] = Field(
        None,
        description="Unused field that is currently always set to `null` and will be removed in the future.\n",
    )
    executedSellAmount: BigUint = Field(
        ...,
        description="The total amount of `sellToken` that has been executed for this order including fees.\n",
    )
    executedSellAmountBeforeFees: BigUint = Field(
        ...,
        description="The total amount of `sellToken` that has been executed for this order without fees.\n",
    )
    executedBuyAmount: BigUint = Field(
        ...,
        description="The total amount of `buyToken` that has been executed for this order.\n",
    )
    executedFeeAmount: BigUint = Field(
        ...,
        description="The total amount of fees that have been executed for this order.",
    )
    invalidated: bool = Field(..., description="Has this order been invalidated?")
    status: OrderStatus = Field(..., description="Order status.")
    fullFeeAmount: Optional[TokenAmount] = Field(
        None, description="Amount that the signed fee would be without subsidies."
    )
    isLiquidityOrder: Optional[bool] = Field(
        None,
        description="Liquidity orders are functionally the same as normal smart contract orders but are not\nplaced with the intent of actively getting traded. Instead they facilitate the\ntrade of normal orders by allowing them to be matched against liquidity orders which\nuses less gas and can have better prices than external liquidity.\n\nAs such liquidity orders will only be used in order to improve settlement of normal\norders. They should not be expected to be traded otherwise and should not expect to get\nsurplus.\n",
    )
    ethflowData: Optional[EthflowData] = None
    onchainUser: Optional[Address] = Field(
        None,
        description="This represents the actual trader of an on-chain order.\n\n### ethflow orders\n\nIn this case, the `owner` would be the `EthFlow` contract and *not* the actual trader.\n",
    )
    onchainOrderData: Optional[OnchainOrderData] = Field(
        None,
        description="There is some data only available for orders that are placed on-chain. This data\ncan be found in this object.\n",
    )
    executedSurplusFee: Optional[BigUint] = Field(
        None, description="Surplus fee that the limit order was executed with."
    )
    fullAppData: Optional[str] = Field(
        None,
        description="Full `appData`, which the contract-level `appData` is a hash of. See `OrderCreation`\nfor more information.\n",
    )


class CompetitionAuction(BaseModel):
    orders: Optional[List[UID]] = Field(
        None, description="The UIDs of the orders included in the auction.\n"
    )
    prices: Optional[AuctionPrices] = None


class OrderCancellations(BaseModel):
    orderUids: Optional[List[UID]] = Field(
        None, description="UIDs of orders to cancel."
    )
    signature: EcdsaSignature = Field(
        ..., description="`OrderCancellation` signed by the owner."
    )
    signingScheme: EcdsaSigningScheme


class OrderCancellation(BaseModel):
    signature: EcdsaSignature = Field(
        ..., description="OrderCancellation signed by owner"
    )
    signingScheme: EcdsaSigningScheme


class Trade(BaseModel):
    blockNumber: int = Field(..., description="Block in which trade occurred.")
    logIndex: int = Field(
        ..., description="Index in which transaction was included in block."
    )
    orderUid: UID = Field(..., description="UID of the order matched by this trade.")
    owner: Address = Field(..., description="Address of trader.")
    sellToken: Address = Field(..., description="Address of token sold.")
    buyToken: Address = Field(..., description="Address of token bought.")
    sellAmount: TokenAmount = Field(
        ...,
        description="Total amount of `sellToken` that has been executed for this trade (including fees).",
    )
    sellAmountBeforeFees: BigUint = Field(
        ...,
        description="The total amount of `sellToken` that has been executed for this order without fees.",
    )
    buyAmount: TokenAmount = Field(
        ..., description="Total amount of `buyToken` received in this trade."
    )
    txHash: TransactionHash = Field(
        ...,
        description="Transaction hash of the corresponding settlement transaction containing the trade (if available).",
    )


class Signature(RootModel[Union[EcdsaSignature, PreSignature]]):
    root: Union[EcdsaSignature, PreSignature] = Field(..., description="A signature.")


class OrderQuoteSide1(BaseModel):
    kind: OrderQuoteSideKindSell
    sellAmountBeforeFee: TokenAmount = Field(
        ...,
        description="The total amount that is available for the order. From this value, the fee\nis deducted and the buy amount is calculated.\n",
    )


class OrderQuoteSide2(BaseModel):
    kind: OrderQuoteSideKindSell
    sellAmountAfterFee: TokenAmount = Field(
        ..., description="The `sellAmount` for the order."
    )


class OrderQuoteSide3(BaseModel):
    kind: OrderQuoteSideKindBuy
    buyAmountAfterFee: TokenAmount = Field(
        ..., description="The `buyAmount` for the order."
    )


class OrderQuoteSide(
    RootModel[Union[OrderQuoteSide1, OrderQuoteSide2, OrderQuoteSide3]]
):
    root: Union[OrderQuoteSide1, OrderQuoteSide2, OrderQuoteSide3] = Field(
        ..., description="The buy or sell side when quoting an order."
    )


class OrderQuoteRequest(BaseModel):
    sellToken: Address = Field(..., description="ERC-20 token to be sold")
    buyToken: Address = Field(..., description="ERC-20 token to be bought")
    receiver: Optional[Address] = Field(
        None,
        description="An optional address to receive the proceeds of the trade instead of the\n`owner` (i.e. the order signer).\n",
    )
    appData: Optional[Union[AppData, AppDataHash]] = Field(
        None,
        description="AppData which will be assigned to the order.\nExpects either a string JSON doc as defined on [AppData](https://github.com/cowprotocol/app-data) or a\nhex encoded string for backwards compatibility.\nWhen the first format is used, it's possible to provide the derived appDataHash field.\n",
    )
    appDataHash: Optional[AppDataHash] = Field(
        None,
        description="The hash of the stringified JSON appData doc.\nIf present, `appData` field must be set with the aforementioned data where this hash is derived from.\nIn case they differ, the call will fail.\n",
    )
    sellTokenBalance: Optional[SellTokenSource] = "erc20"
    buyTokenBalance: Optional[BuyTokenDestination] = "erc20"
    from_: Address = Field(..., alias="from")
    priceQuality: Optional[PriceQuality] = "verified"
    signingScheme: Optional[SigningScheme] = "eip712"
    onchainOrder: Optional[Any] = Field(
        False,
        description='Flag to signal whether the order is intended for on-chain order placement. Only valid\nfor non ECDSA-signed orders."\n',
    )


class OrderQuoteResponse(BaseModel):
    quote: OrderParameters
    from_: Optional[Address] = Field(None, alias="from")
    expiration: str = Field(
        ...,
        description="Expiration date of the offered fee. Order service might not accept\nthe fee after this expiration date. Encoded as ISO 8601 UTC.\n",
        examples=["1985-03-10T18:35:18.814523Z"],
    )
    id: Optional[int] = Field(
        None,
        description="Quote ID linked to a quote to enable providing more metadata when analysing\norder slippage.\n",
    )
    verified: bool = Field(
        ...,
        description="Whether it was possible to verify that the quoted amounts are accurate using a simulation.\n",
    )


class SolverCompetitionResponse(BaseModel):
    auctionId: Optional[int] = Field(
        None, description="The ID of the auction the competition info is for."
    )
    transactionHash: Optional[TransactionHash] = Field(
        None,
        description="The hash of the transaction that the winning solution of this info was submitted in.",
    )
    gasPrice: Optional[float] = Field(
        None, description="Gas price used for ranking solutions."
    )
    liquidityCollectedBlock: Optional[int] = None
    competitionSimulationBlock: Optional[int] = None
    auction: Optional[CompetitionAuction] = None
    solutions: Optional[List[SolverSettlement]] = Field(
        None,
        description="Maps from solver name to object describing that solver's settlement.",
    )


class OrderCreation(BaseModel):
    sellToken: Address = Field(..., description="see `OrderParameters::sellToken`")
    buyToken: Address = Field(..., description="see `OrderParameters::buyToken`")
    receiver: Optional[Address] = Field(
        None, description="see `OrderParameters::receiver`"
    )
    sellAmount: TokenAmount = Field(
        ..., description="see `OrderParameters::sellAmount`"
    )
    buyAmount: TokenAmount = Field(..., description="see `OrderParameters::buyAmount`")
    validTo: int = Field(..., description="see `OrderParameters::validTo`")
    feeAmount: TokenAmount = Field(..., description="see `OrderParameters::feeAmount`")
    kind: OrderKind = Field(..., description="see `OrderParameters::kind`")
    partiallyFillable: bool = Field(
        ..., description="see `OrderParameters::partiallyFillable`"
    )
    sellTokenBalance: Optional[SellTokenSource] = Field(
        "erc20", description="see `OrderParameters::sellTokenBalance`"
    )
    buyTokenBalance: Optional[BuyTokenDestination] = Field(
        "erc20", description="see `OrderParameters::buyTokenBalance`"
    )
    signingScheme: SigningScheme
    signature: Signature
    from_: Optional[Address] = Field(
        None,
        alias="from",
        description="If set, the backend enforces that this address matches what is decoded as the *signer* of\nthe signature. This helps catch errors with invalid signature encodings as the backend\nmight otherwise silently work with an unexpected address that for example does not have\nany balance.\n",
    )
    quoteId: Optional[int] = Field(
        None,
        description="Orders can optionally include a quote ID. This way the order can be linked to a quote\nand enable providing more metadata when analysing order slippage.\n",
    )
    appData: Union[AppData, AppDataHash] = Field(
        ...,
        description="This field comes in two forms for backward compatibility. The hash form will eventually \nstop being accepted.\n",
    )
    appDataHash: Optional[AppDataHash] = Field(
        None,
        description="May be set for debugging purposes. If set, this field is compared to what the backend\ninternally calculates as the app data hash based on the contents of `appData`. If the\nhash does not match, an error is returned. If this field is set, then `appData` **MUST** be\na string encoding of a JSON object.\n",
    )


class Order(OrderCreation, OrderMetaData):
    pass


class AuctionOrder(BaseModel):
    uid: UID
    sellToken: Address = Field(..., description="see `OrderParameters::sellToken`")
    buyToken: Address = Field(..., description="see `OrderParameters::buyToken`")
    sellAmount: TokenAmount = Field(
        ..., description="see `OrderParameters::sellAmount`"
    )
    buyAmount: TokenAmount = Field(..., description="see `OrderParameters::buyAmount`")
    userFee: TokenAmount = Field(..., description="see `OrderParameters::feeAmount`")
    validTo: int = Field(..., description="see `OrderParameters::validTo`")
    kind: OrderKind = Field(..., description="see `OrderParameters::kind`")
    receiver: Address = Field(..., description="see `OrderParameters::receiver`")
    owner: Address
    partiallyFillable: bool = Field(
        ..., description="see `OrderParameters::partiallyFillable`"
    )
    executed: TokenAmount = Field(
        ...,
        description="Currently executed amount of sell/buy token, depending on the order kind.\n",
    )
    preInteractions: List[InteractionData] = Field(
        ...,
        description="The pre-interactions that need to be executed before the first execution of the order.\n",
    )
    postInteractions: List[InteractionData] = Field(
        ...,
        description="The post-interactions that need to be executed after the execution of the order.\n",
    )
    sellTokenBalance: SellTokenSource = Field(
        ..., description="see `OrderParameters::sellTokenBalance`"
    )
    buyTokenBalance: BuyTokenDestination = Field(
        ..., description="see `OrderParameters::buyTokenBalance`"
    )
    class_: OrderClass = Field(..., alias="class")
    appData: AppDataHash
    signature: Signature
    protocolFees: List[FeePolicy] = Field(
        ...,
        description="The fee policies that are used to compute the protocol fees for this order.\n",
    )


class Auction(BaseModel):
    id: Optional[int] = Field(
        None,
        description="The unique identifier of the auction. Increment whenever the backend creates a new auction.\n",
    )
    block: Optional[int] = Field(
        None,
        description="The block number for the auction. Orders and prices are guaranteed to be valid on this\nblock. Proposed settlements should be valid for this block as well.\n",
    )
    latestSettlementBlock: Optional[int] = Field(
        None,
        description="The latest block on which a settlement has been processed.\n\n**NOTE**: Under certain conditions it is possible for a settlement to have been mined as\npart of `block` but not have yet been processed.\n",
    )
    orders: Optional[List[AuctionOrder]] = Field(
        None, description="The solvable orders included in the auction.\n"
    )
    prices: Optional[AuctionPrices] = None