import sys
import os
from pathlib import Path
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Path Fix: Add root to sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from src.models import DharmaGCN

# Initialize FastAPI
app = FastAPI(title="Dharma-Debt Nexus API")

# 2. Load Model
INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM = 3, 16, 2
model = DharmaGCN(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)

WEIGHTS_PATH = os.path.join(root_path, "models", "dharma_weights.pth")

if os.path.exists(WEIGHTS_PATH):
    # PyTorch 2.6 security Best Practice
    model.load_state_dict(torch.load(WEIGHTS_PATH, weights_only=True))
    model.eval()
    print("✅ GNN weights loaded successfully.")
else:
    print(f"❌ Weights not found at {WEIGHTS_PATH}")

# 3. Input Schema
class BorrowerRequest(BaseModel):
    age: float
    income: float
    dharma_score: float

# 4. Root Route (Greeting)
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Dharma-Debt Nexus API! Go to /docs to test predictions.",
        "status": "Online"
    }

# 5. Prediction Route
@app.post("/predict")
async def predict_risk(borrower: BorrowerRequest):
    try:
        # Prepare input tensor
        x = torch.tensor([[borrower.age, borrower.income, borrower.dharma_score]], dtype=torch.float)
        
        # Self-loop for single node inference
        dummy_edge_index = torch.tensor([[0], [0]], dtype=torch.long)
        
        with torch.no_grad():
            # This calls model.forward(x, dummy_edge_index)
            logits = model(x, dummy_edge_index)
            prediction = torch.exp(logits).argmax(dim=1).item()
        
        risk_label = "High Risk (Default)" if prediction == 1 else "Safe (Recoverable)"
        
        return {
            "status": "success",
            "prediction": risk_label,
            "data": borrower
        }
    except Exception as e:
        # Send the specific error to Swagger for easier debugging
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)