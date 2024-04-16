import pytest
import unittest
from unittest.mock import patch
from cow_py.codegen.components.base_contract import (
    BaseContract,
    Chain,
)  # Adjust the import statement according to your actual module structure


CONTRACT_EXAMPLE_ADDRESS = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"


class TestBaseContract(unittest.TestCase):
    @patch(
        "cow_py.codegen.components.base_contract.ContractLoader"
    )  # Mocking ContractLoader to avoid actual web3 calls
    def test_base_contract_singleton(self, mock_loader):
        address = CONTRACT_EXAMPLE_ADDRESS
        chain = Chain.MAINNET
        contract1 = BaseContract(address, chain)
        contract2 = BaseContract(address, chain)
        self.assertIs(
            contract1,
            contract2,
            "BaseContract should return the same instance for the same address and chain",
        )

    def test_base_contract_function_exists_in_abi(self):
        contract = BaseContract(
            CONTRACT_EXAMPLE_ADDRESS,
            Chain.MAINNET,
            [{"type": "function", "name": "balanceOf"}],
        )
        pytest.set_trace()
        self.assertTrue(contract._function_exists_in_abi("balanceOf"))
        self.assertFalse(contract._function_exists_in_abi("transfer"))

    def test_base_contract_event_exists_in_abi(self):
        contract = BaseContract(
            CONTRACT_EXAMPLE_ADDRESS,
            Chain.MAINNET,
            [{"type": "event", "name": "Transfer"}],
        )
        print(contract.web3_contract.abi, "oi")
        self.assertTrue(contract._event_exists_in_abi("Transfer"))
        self.assertFalse(contract._event_exists_in_abi("Approval"))

    # @patch("cow_py.codegen.components.base_contract.ContractLoader")
    # def test_base_contract_getattr(self, mock_loader):
    #     mock_loader.return_value.get_web3_contract.return_value = Mock(
    #         address=CONTRACT_EXAMPLE_ADDRESS,
    #         abi=[
    #             {"type": "function", "name": "balanceOf"},
    #             {"type": "event", "name": "Transfer"},
    #         ],
    #         functions=Mock(balanceOf=Mock(call=Mock(return_value="1000"))),
    #         events=Mock(Transfer=Mock(filter=Mock(return_value=[]))),
    #     )
    #     contract = BaseContract(CONTRACT_EXAMPLE_ADDRESS, Chain.MAINNET)
    #     self.assertEqual(contract.balanceOf(), "1000")
    #     self.assertIsNotNone(contract.Transfer)
    #     with self.assertRaises(AttributeError):
    #         _ = contract.nonExistentMethod
