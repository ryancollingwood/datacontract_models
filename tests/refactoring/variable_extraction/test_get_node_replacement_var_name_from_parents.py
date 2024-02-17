import ast

from refactoring.variable_extraction import node_replacement_var_name_from_parents


def test_get_node_replacement_var_name_from_parents_with_inline_call():
    code_str = """Container(
    name="Bag of holding",
    contents=[
        Item(
            name="marbles",
        )
    ]
    )
"""
    expected = "bag_of_holding_marbles"

    module = ast.parse(code_str)
    test_node = module.body[0].value.keywords[1].value.elts[0].keywords[0]
    assert ast.dump(test_node) == "keyword(arg='name', value=Constant(value='marbles'))"

    result = node_replacement_var_name_from_parents(
        ["Container", "Item"],
        dict(),
        module,
        test_node,
    )

    assert result == expected
