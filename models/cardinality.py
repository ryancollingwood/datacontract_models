from .meta_schema_enum import MetaSchemaEnum

class Cardinality(MetaSchemaEnum):
  ONLY_ONE = "OnlyOne"
  ONE_OR_MORE = "OneOrMore"
  ZERO_OR_ONE = "ZeroOrOne"
  ZERO_OR_MANY = "ZeroOrMany"