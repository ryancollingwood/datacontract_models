from pydantic import BaseModel, ConfigDict, Extra

class CaptureSheetBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        validate_default=True, 
        extra=Extra.allow,
        # this allows us to populate a field by it's alias
        populate_by_name=True,
    )
