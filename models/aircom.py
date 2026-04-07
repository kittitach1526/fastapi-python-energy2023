from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class AirComDetail(BaseModel):
    aircom_id: str
    pressure: float
    temp: float
    power_ac: float
    total_run: float
    delay: float
    state: str
    warning: str
    danger: str


class PressureDetail(BaseModel):
    pressure_id: str
    value: float


class FlowRateDetail(BaseModel):
    flow_id: str
    flow_rate: float
    flow_total: float


class StatusDetail(BaseModel):
    status_id: str
    status: str


class AirComSchema(BaseModel):
    time: datetime = Field(default_factory=datetime.utcnow)
    aircoms: List[AirComDetail]
    pressures: List[PressureDetail]
    flowrates: List[FlowRateDetail]
    statuses: List[StatusDetail]