import enum

class Cardinality(enum.Enum):
  ONLY_ONE = "OnlyOne"
  ONE_OR_MORE = "OneOrMore"
  ZERO_OR_ONE = "ZeroOrOne"
  ZERO_OR_MANY = "ZeroOrMany"