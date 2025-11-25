from pydantic import BaseModel, Field


class EtaRequest(BaseModel):
    distance_km: float = Field(..., ge=0)
    prep_time_min: float = Field(..., ge=0)
    estimated_travel_time_min: float = Field(..., ge=0)
    hour_of_day: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    is_raining: int = Field(..., ge=0, le=1)
    courier_experience: int = Field(..., ge=0, le=2)


class EtaResponse(BaseModel):
    predicted_eta_min: float
    delay_probability: float
    risk_tag: str
