from .meta_schema_enum import MetaSchemaEnum


class Cardinality(MetaSchemaEnum):
    ONLY_ONE = "OnlyOne"
    ONE_OR_MORE = "OneOrMore"
    ZERO_OR_ONE = "ZeroOrOne"
    ZERO_OR_MANY = "ZeroOrMany"

    def is_mandatory(self):
        return self in [Cardinality.ONLY_ONE, Cardinality.ONE_OR_MORE]
    
    def is_optional(self):
        return not self.is_mandatory()
    
    def is_singular(self):
        return self in [Cardinality.ONLY_ONE, Cardinality.ZERO_OR_ONE]