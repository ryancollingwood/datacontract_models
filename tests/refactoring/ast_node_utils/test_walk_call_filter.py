import ast
from tests.refactoring.code_examples import unrefactored_code_ast
from refactoring.ast_node_utils import walk_call_filter


def test_walk_call_filter_single_class_get_one():
    unparsed_expected = [
        "item=Item(name='Cheese')",
    ]

    dumped_expected = [
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=30, col_offset=19, end_lineno=30, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=31, col_offset=21, end_lineno=31, end_col_offset=29), lineno=31, col_offset=14, end_lineno=31, end_col_offset=29)], lineno=30, col_offset=19, end_lineno=32, end_col_offset=13), lineno=30, col_offset=12, end_lineno=32, end_col_offset=13)",
    ]

    results = walk_call_filter(unrefactored_code_ast(), ["Item"], max_items=1)

    assert len(results) == 1

    assert [ast.unparse(x) for x in results] == unparsed_expected

    assert [ast.dump(x, annotate_fields = True, include_attributes = True) for x in results] == dumped_expected



def test_walk_call_filter_single_class_get_all():
    unparsed_expected = [
        "item=Item(name='Cheese')",
        "item=Item(name='Cheese')",
        "item=Item(name='Beer')",
        "item=Item(name='Beer')",
        "item=Item(name='Spell Book')",
        "item=Item(name='Cheese')",
        "item=Item(name='Arrow')",
    ]

    dumped_expected = [
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=30, col_offset=19, end_lineno=30, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=31, col_offset=21, end_lineno=31, end_col_offset=29), lineno=31, col_offset=14, end_lineno=31, end_col_offset=29)], lineno=30, col_offset=19, end_lineno=32, end_col_offset=13), lineno=30, col_offset=12, end_lineno=32, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=47, col_offset=19, end_lineno=47, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=48, col_offset=21, end_lineno=48, end_col_offset=29), lineno=48, col_offset=14, end_lineno=48, end_col_offset=29)], lineno=47, col_offset=19, end_lineno=49, end_col_offset=13), lineno=47, col_offset=12, end_lineno=49, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=53, col_offset=19, end_lineno=53, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Beer', lineno=54, col_offset=21, end_lineno=54, end_col_offset=27), lineno=54, col_offset=14, end_lineno=54, end_col_offset=27)], lineno=53, col_offset=19, end_lineno=55, end_col_offset=13), lineno=53, col_offset=12, end_lineno=55, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=70, col_offset=19, end_lineno=70, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Beer', lineno=71, col_offset=21, end_lineno=71, end_col_offset=27), lineno=71, col_offset=14, end_lineno=71, end_col_offset=27)], lineno=70, col_offset=19, end_lineno=72, end_col_offset=13), lineno=70, col_offset=12, end_lineno=72, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=76, col_offset=19, end_lineno=76, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Spell Book', lineno=77, col_offset=21, end_lineno=77, end_col_offset=33), lineno=77, col_offset=14, end_lineno=77, end_col_offset=33)], lineno=76, col_offset=19, end_lineno=78, end_col_offset=13), lineno=76, col_offset=12, end_lineno=78, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=93, col_offset=19, end_lineno=93, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=94, col_offset=21, end_lineno=94, end_col_offset=29), lineno=94, col_offset=14, end_lineno=94, end_col_offset=29)], lineno=93, col_offset=19, end_lineno=95, end_col_offset=13), lineno=93, col_offset=12, end_lineno=95, end_col_offset=13)",
        "keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=99, col_offset=19, end_lineno=99, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Arrow', lineno=100, col_offset=21, end_lineno=100, end_col_offset=28), lineno=100, col_offset=14, end_lineno=100, end_col_offset=28)], lineno=99, col_offset=19, end_lineno=101, end_col_offset=13), lineno=99, col_offset=12, end_lineno=101, end_col_offset=13)",
    ]

    results = walk_call_filter(unrefactored_code_ast(), ["Item"])

    assert [ast.unparse(x) for x in results] == unparsed_expected

    assert [ast.dump(x, annotate_fields = True, include_attributes = True) for x in results] == dumped_expected


def test_walk_call_filter_class_in_lists():
    """
    This tests that we can retrieve occurances inside a list
    """
    unparsed_expected = [
        "InventoryItem(item=Item(name='Cheese'), quantity=3)",
        "InventoryItem(item=Item(name='Cheese'), quantity=1)",
        "InventoryItem(item=Item(name='Beer'), quantity=1)",
        "InventoryItem(item=Item(name='Beer'), quantity=3)",
        "InventoryItem(item=Item(name='Spell Book'), quantity=1)",
        "InventoryItem(item=Item(name='Cheese'), quantity=1)",
        "InventoryItem(item=Item(name='Arrow'), quantity=99)",
    ]

    dumped_expected = [
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=29, col_offset=8, end_lineno=29, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=30, col_offset=19, end_lineno=30, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=31, col_offset=21, end_lineno=31, end_col_offset=29), lineno=31, col_offset=14, end_lineno=31, end_col_offset=29)], lineno=30, col_offset=19, end_lineno=32, end_col_offset=13), lineno=30, col_offset=12, end_lineno=32, end_col_offset=13), keyword(arg='quantity', value=Constant(value=3, lineno=33, col_offset=23, end_lineno=33, end_col_offset=24), lineno=33, col_offset=12, end_lineno=33, end_col_offset=24)], lineno=29, col_offset=8, end_lineno=34, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=46, col_offset=8, end_lineno=46, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=47, col_offset=19, end_lineno=47, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=48, col_offset=21, end_lineno=48, end_col_offset=29), lineno=48, col_offset=14, end_lineno=48, end_col_offset=29)], lineno=47, col_offset=19, end_lineno=49, end_col_offset=13), lineno=47, col_offset=12, end_lineno=49, end_col_offset=13), keyword(arg='quantity', value=Constant(value=1, lineno=50, col_offset=23, end_lineno=50, end_col_offset=24), lineno=50, col_offset=12, end_lineno=50, end_col_offset=24)], lineno=46, col_offset=8, end_lineno=51, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=52, col_offset=8, end_lineno=52, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=53, col_offset=19, end_lineno=53, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Beer', lineno=54, col_offset=21, end_lineno=54, end_col_offset=27), lineno=54, col_offset=14, end_lineno=54, end_col_offset=27)], lineno=53, col_offset=19, end_lineno=55, end_col_offset=13), lineno=53, col_offset=12, end_lineno=55, end_col_offset=13), keyword(arg='quantity', value=Constant(value=1, lineno=56, col_offset=23, end_lineno=56, end_col_offset=24), lineno=56, col_offset=12, end_lineno=56, end_col_offset=24)], lineno=52, col_offset=8, end_lineno=57, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=69, col_offset=8, end_lineno=69, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=70, col_offset=19, end_lineno=70, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Beer', lineno=71, col_offset=21, end_lineno=71, end_col_offset=27), lineno=71, col_offset=14, end_lineno=71, end_col_offset=27)], lineno=70, col_offset=19, end_lineno=72, end_col_offset=13), lineno=70, col_offset=12, end_lineno=72, end_col_offset=13), keyword(arg='quantity', value=Constant(value=3, lineno=73, col_offset=23, end_lineno=73, end_col_offset=24), lineno=73, col_offset=12, end_lineno=73, end_col_offset=24)], lineno=69, col_offset=8, end_lineno=74, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=75, col_offset=8, end_lineno=75, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=76, col_offset=19, end_lineno=76, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Spell Book', lineno=77, col_offset=21, end_lineno=77, end_col_offset=33), lineno=77, col_offset=14, end_lineno=77, end_col_offset=33)], lineno=76, col_offset=19, end_lineno=78, end_col_offset=13), lineno=76, col_offset=12, end_lineno=78, end_col_offset=13), keyword(arg='quantity', value=Constant(value=1, lineno=79, col_offset=23, end_lineno=79, end_col_offset=24), lineno=79, col_offset=12, end_lineno=79, end_col_offset=24)], lineno=75, col_offset=8, end_lineno=80, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=92, col_offset=8, end_lineno=92, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=93, col_offset=19, end_lineno=93, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Cheese', lineno=94, col_offset=21, end_lineno=94, end_col_offset=29), lineno=94, col_offset=14, end_lineno=94, end_col_offset=29)], lineno=93, col_offset=19, end_lineno=95, end_col_offset=13), lineno=93, col_offset=12, end_lineno=95, end_col_offset=13), keyword(arg='quantity', value=Constant(value=1, lineno=96, col_offset=23, end_lineno=96, end_col_offset=24), lineno=96, col_offset=12, end_lineno=96, end_col_offset=24)], lineno=92, col_offset=8, end_lineno=97, end_col_offset=9)",
        "Call(func=Name(id='InventoryItem', ctx=Load(), lineno=98, col_offset=8, end_lineno=98, end_col_offset=21), args=[], keywords=[keyword(arg='item', value=Call(func=Name(id='Item', ctx=Load(), lineno=99, col_offset=19, end_lineno=99, end_col_offset=23), args=[], keywords=[keyword(arg='name', value=Constant(value='Arrow', lineno=100, col_offset=21, end_lineno=100, end_col_offset=28), lineno=100, col_offset=14, end_lineno=100, end_col_offset=28)], lineno=99, col_offset=19, end_lineno=101, end_col_offset=13), lineno=99, col_offset=12, end_lineno=101, end_col_offset=13), keyword(arg='quantity', value=Constant(value=99, lineno=102, col_offset=23, end_lineno=102, end_col_offset=25), lineno=102, col_offset=12, end_lineno=102, end_col_offset=25)], lineno=98, col_offset=8, end_lineno=103, end_col_offset=9)",
    ]

    results = walk_call_filter(unrefactored_code_ast(), ["InventoryItem"])

    assert [ast.unparse(x) for x in results] == unparsed_expected

    assert [ast.dump(x, annotate_fields = True, include_attributes = True) for x in results] == dumped_expected
    
     