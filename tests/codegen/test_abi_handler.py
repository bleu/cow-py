import pytest

from cow_py.codegen.abi_handler import to_python_conventional_name


@pytest.mark.parametrize(
    "input_name, expected_output",
    [
        # ("GPv2Order_Data", "gp_v2_order_data"),
        ("simpleTest", "simple_test"),
        ("ThisIsATest", "this_is_a_test"),
        ("number2IsHere", "number_2_is_here"),
        ("AnotherTest123", "another_test_123"),
        ("JSONData", "json_data"),
        # ("GPv2Order_Data_arg_1", "gp_v2_order_data_arg_1"),
    ],
)
def test_to_python_conventional_name(input_name, expected_output):
    assert to_python_conventional_name(input_name) == expected_output


def test_compile_partial():
    # Test that compile_partial correctly compiles a partial template
    pass


def test_get_filename_without_extension():
    # Test that get_filename_without_extension correctly removes the extension
    pass


def test_get_template_file():
    # Test that _get_template_file returns the correct template file path
    pass


def test_get_partials_files():
    # Test that _get_partials_files returns the correct list of partial files
    pass


def test_abi_handler_generate():
    # Test that ABIHandler.generate correctly generates Python code from an ABI
    pass


def test_abi_handler_prepare_template_data():
    # Test that ABIHandler._prepare_template_data correctly processes the ABI
    pass


def test_abi_handler_process_parameters():
    # Test that ABIHandler._process_parameters correctly processes function parameters
    pass


def test_abi_handler_process_function():
    # Test that ABIHandler._process_function correctly processes a function item
    pass


def test_abi_handler_render_template():
    # Test that ABIHandler._render_template correctly renders the template with data
    pass
