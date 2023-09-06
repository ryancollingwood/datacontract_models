from pydantic import BaseModel, ConfigDict, Extra


class MetaSchemaBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        anystr_lower=True, validate_all=True, extra=Extra.ignore

      )

    name: str