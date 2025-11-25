from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import EtaRequest, EtaResponse
from .model_loader import EtaModelService

app = FastAPI(
    title="Smart Delivery ETA API",
    description="Predict delivery ETA and delay risk for food delivery orders.",
    version="1.0.0",
)

# Enable CORS so Streamlit / frontend can call this easily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in real life, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_service = EtaModelService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict-eta", response_model=EtaResponse)
def predict_eta(req: EtaRequest):
    eta_pred, delay_proba, risk_tag = model_service.predict(req.dict())
    return EtaResponse(
        predicted_eta_min=round(eta_pred, 1),
        delay_probability=round(delay_proba, 4),
        risk_tag=risk_tag,
    )
