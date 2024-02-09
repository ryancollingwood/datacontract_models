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

def unrefactored_code_ast():
    return ast.parse(unrefactored_code_str)