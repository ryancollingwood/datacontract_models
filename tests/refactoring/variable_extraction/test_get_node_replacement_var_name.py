import ast

from refactoring.variable_extraction import get_node_replacement_var_name


def test_get_node_replacement_var_name_from_expression():
    code_str = """Singer(
    name="Billy Idol",
)"""
    expected = "singer_billy_idol"

    ast_node = ast.parse(code_str).body[0]
    result = get_node_replacement_var_name(ast_node, "Singer")

    assert result == expected


def test_get_node_replacement_var_name_from_expression_with_extra_spaces():
    code_str = """Singer(
    name="Andrew W  K",
)"""
    expected = "singer_andrew_w_k"

    ast_node = ast.parse(code_str).body[0]
    result = get_node_replacement_var_name(ast_node, "Singer")

    assert result == expected

def test_get_node_replacement_var_name_from_expression_with_but_no_name():
    code_str = """Peaches(
    origin="factory downtown",
    contained="in a can",
    )
"""
    expected = "fruit_factory_downtown_in_a_can"
    
    ast_node = ast.parse(code_str).body[0]
    result = get_node_replacement_var_name(ast_node, "fruit")
    
    assert result == expected
