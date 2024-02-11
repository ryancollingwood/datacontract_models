import ast

unrefactored_code_str = """from typing import List
from pydantic import BaseModel

class CharacterClass(BaseModel):
  name: str
  is_ranged: bool
  is_magic: bool

class Item(BaseModel):
  name: str

class InventoryItem(BaseModel):
  item: Item
  quantity: int

class Character(BaseModel):
  name: str
  char_class: CharacterClass
  inventory: List[InventoryItem]

fred = Character(
    name = "fred",
    char_class = CharacterClass(
        name = "warrior",
        is_ranged = False,
        is_magic = False
    ),
    inventory = [
        InventoryItem(
            item = Item(
              name = "Cheese",
            ),
            quantity = 3
        )
    ]
)

sarah = Character(
    name = "sarah",
    char_class = CharacterClass(
        name = "warrior",
        is_ranged = False,
        is_magic = False
    ),
    inventory = [
        InventoryItem(
            item = Item(
              name = "Cheese",
            ),
            quantity = 1
        ),
        InventoryItem(
            item = Item(
              name = "Beer",
            ),
            quantity = 1
        ),
    ]
)

barry = Character(
    name = "barry",
    char_class = CharacterClass(
        name = "mage",
        is_ranged = True,
        is_magic = True
    ),
    inventory = [
        InventoryItem(
            item = Item(
              name = "Beer",
            ),
            quantity = 3
        ),
        InventoryItem(
            item = Item(
              name = "Spell Book",
            ),
            quantity = 1
        ),
    ]
)

lydia = Character(
    name = "lydia",
    char_class = CharacterClass(
        name = "ranger",
        is_ranged = True,
        is_magic = False
    ),
    inventory = [
        InventoryItem(
            item = Item(
              name = "Cheese",
            ),
            quantity = 1
        ),
        InventoryItem(
            item = Item(
              name = "Arrow",
            ),
            quantity = 99
        ),
    ]
)
"""

refactored_code = """from typing import List
from pydantic import BaseModel

class CharacterClass(BaseModel):
  name: str
  is_ranged: bool
  is_magic: bool

class Item(BaseModel):
  name: str

class InventoryItem(BaseModel):
  item: Item
  quantity: int

class Character(BaseModel):
  name: str
  char_class: CharacterClass
  inventory: List[InventoryItem]


item_cheese = Item(name="Cheese")
characterclass_warrior = CharacterClass(name="warrior", is_ranged=False, is_magic=False)
fred = Character(
    name="fred",
    char_class=characterclass_warrior,
    inventory=[InventoryItem(item=item_cheese, quantity=3)],
)
item_beer = Item(name="Beer")
sarah = Character(
    name="sarah",
    char_class=characterclass_warrior,
    inventory=[
        InventoryItem(item=item_cheese, quantity=1),
        InventoryItem(item=item_beer, quantity=1),
    ],
)
item_spell_book = Item(name="Spell Book")
characterclass_mage = CharacterClass(name="mage", is_ranged=True, is_magic=True)
barry = Character(
    name="barry",
    char_class=characterclass_mage,
    inventory=[
        InventoryItem(item=item_beer, quantity=3),
        InventoryItem(item=item_spell_book, quantity=1),
    ],
)
item_arrow = Item(name="Arrow")
characterclass_ranger = CharacterClass(name="ranger", is_ranged=True, is_magic=False)
lydia = Character(
    name="lydia",
    char_class=characterclass_ranger,
    inventory=[
        InventoryItem(item=item_cheese, quantity=1),
        InventoryItem(item=item_arrow, quantity=99),
    ],
)
"""

def unrefactored_code_ast():
    return ast.parse(unrefactored_code_str)

def refactored_code_ast():
    return ast.parse(refactored_code)