from models.cardinality import Cardinality
from models.meta_schema import Actor
from .capture_sheet_base_model import CaptureSheetBaseModel

class LastEvent(CaptureSheetBaseModel):
    name: str
    raised_by: Actor
    received_by: Actor

class LastAggregate(CaptureSheetBaseModel):
    name: str
    cardinality: Cardinality