from pydantic import BaseModel, ConfigDict, Extra

class CaptureSheetBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        str_to_lower=True, validate_default=True, extra=Extra.ignore
    )
