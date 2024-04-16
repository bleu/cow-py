import pytest
from unittest.mock import patch, Mock
from cow_py.codegen.components.base_contract import (
    BaseContract,
    Chain,
)  # Adjust the import statement according to your actual module structure


# Test for Singleton Pattern
@patch(
    "cow_py.codegen.components.base_contract.ContractLoader"
)  # Mocking ContractLoader to avoid actual web3 calls
def test_base_contract_singleton(mock_loader):
    address = "0x123"
    chain = Chain.MAINNET
    contract1 = BaseContract(address, chain)
    contract2 = BaseContract(address, chain)
    assert (
        contract1 is contract2
    ), "BaseContract should return the same instance for the same address and chain"


@pytest.fixture
def contract_with_abi():
    abi = [
        {"type": "function", "name": "balanceOf"},
        {"type": "event", "name": "Transfer"},
    ]
    with patch(
        "cow_py.codegen.components.contract_loader.ContractLoader"
    ) as mock_loader:
        mock_contract = Mock()
        mock_contract.abi = abi
        mock_loader.return_value.get_web3_contract.return_value = mock_contract
        contract = BaseContract("0x123", Chain.MAINNET, abi)
    return contract


def test_base_contract_function_exists_in_abi(contract_with_abi):
    assert contract_with_abi._function_exists_in_abi("balanceOf")
    assert not contract_with_abi._function_exists_in_abi("transfer")


# def test_base_contract_event_exists_in_abi(contract_with_abi):
#     assert contract_with_abi._event_exists_in_abi("Transfer")
#     assert not contract_with_abi._event_exists_in_abi("Approval")


# @patch("cow_py.codegen.components.base_contract.ContractLoader")
# def test_base_contract_getattr(mock_loader):
#     mock_contract = Mock()
#     mock_contract.address = "0x123"
#     mock_contract.abi = [
#         {"type": "function", "name": "balanceOf"},
#         {"type": "event", "name": "Transfer"},
#     ]
#     mock_contract.functions.balanceOf = Mock(
#         return_value=Mock(call=Mock(return_value="1000"))
#     )
#     mock_contract.events.Transfer = Mock(filter=Mock(return_value=[]))

#     mock_loader.return_value.get_web3_contract.return_value = mock_contract

#     contract = BaseContract("0x123", Chain.MAINNET)
#     assert (
#         contract.balanceOf() == "1000"
#     ), "Failed to mock balanceOf function call properly"
#     assert hasattr(contract, "Transfer"), "Event 'Transfer' should be accessible"
#     with pytest.raises(AttributeError):
#         _ = contract.nonExistentMethod
