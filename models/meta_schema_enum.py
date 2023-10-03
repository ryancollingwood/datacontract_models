import enum

"""
Due to way python implements enums, you cannot extend an child enum 
class if the parent class has enum values set. This is a workaround 
to ensure we have consistent way for comparing "unspecified" values

On child classes, it would look like this:
```python
from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE

class MyEnum(MetaSchemaEnum):
    UNSPECIFIED = UNSPECIFIED_VALUE
    MY_VALUE = "my_value"
```
"""
UNSPECIFIED_VALUE = "UNSPECIFIED"

class MetaSchemaEnum(enum.Enum):

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{type(self).__name__}.{str(self.name)}"
    
    def is_specified(self):
        return all([
            self.value is not None,
            self.value != "",
            self.value != UNSPECIFIED_VALUE,
        ])