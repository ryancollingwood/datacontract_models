import ast
from tests.refactoring.code_examples import unrefactored_code_ast
from refactoring.ast_node_utils import walk_assign_filter

def test_walk_assign_filter():
    expected_unparsed = [
        "fred = Character(name='fred', char_class=CharacterClass(name='warrior', is_ranged=False, is_magic=False), inventory=[InventoryItem(item=Item(name='Cheese'), quantity=3)])",
        "sarah = Character(name='sarah', char_class=CharacterClass(name='warrior', is_ranged=False, is_magic=False), inventory=[InventoryItem(item=Item(name='Cheese'), quantity=1), InventoryItem(item=Item(name='Beer'), quantity=1)])",
        "barry = Character(name='barry', char_class=CharacterClass(name='mage', is_ranged=True, is_magic=True), inventory=[InventoryItem(item=Item(name='Beer'), quantity=3), InventoryItem(item=Item(name='Spell Book'), quantity=1)])",
        "lydia = Character(name='lydia', char_class=CharacterClass(name='ranger', is_ranged=True, is_magic=False), inventory=[InventoryItem(item=Item(name='Cheese'), quantity=1), InventoryItem(item=Item(name='Arrow'), quantity=99)])",
    ]

    expected_names = ['fred', 'sarah', 'barry', 'lydia']

    results = walk_assign_filter(unrefactored_code_ast(), ["Character"])
    
    assert [ast.unparse(x) for x in results]  == expected_unparsed
    
    assert [x.targets[0].id for x in results] == expected_names

    assert all([len(x.targets) == 1 for x in results])
