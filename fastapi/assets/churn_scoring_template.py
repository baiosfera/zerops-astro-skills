import asyncio
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter(prefix="/api/v1/predict", tags=["AI Inference"])

class CustomerScoringInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str
    recency_days: int = Field(..., ge=0)
    frequency_purchases: int = Field(..., ge=0)
    monetary_value: float = Field(..., ge=0.0)
    support_tickets: int = Field(default=0, ge=0)

class CustomerScoringOutput(BaseModel):
    customer_id: str
    lead_score: int
    churn_risk_probability: float
    segment: str

@router.post("/score", response_model=CustomerScoringOutput)
async def score_customer(payload: CustomerScoringInput, request: Request) -> CustomerScoringOutput:
    model = getattr(request.app.state, "churn_classifier", None)
    
    # Inferencia en threadpool para no bloquear bucle ASGI
    def _calculate():
        if model:
            prob = float(model.predict_proba([[payload.recency_days, payload.frequency_purchases, payload.monetary_value, payload.support_tickets]])[0][1])
        else:
            # Heurística RFM de fallback si el modelo no está precargado
            score_base = min(100, int((payload.frequency_purchases * 20) + (payload.monetary_value / 50) - (payload.recency_days * 0.5) - (payload.support_tickets * 10)))
            prob = max(0.0, min(1.0, 1.0 - (score_base / 100)))
            
        score = max(0, min(100, int((1.0 - prob) * 100)))
        seg = "VIP" if score > 80 else ("En Riesgo" if prob > 0.6 else "Activo")
        return score, prob, seg

    score, prob, seg = await asyncio.to_thread(_calculate)
    return CustomerScoringOutput(
        customer_id=payload.customer_id,
        lead_score=score,
        churn_risk_probability=round(prob, 4),
        segment=seg
    )
