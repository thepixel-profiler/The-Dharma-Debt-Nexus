from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import sys
from pathlib import Path
#from src.models import DharmaGCN
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
app = FastAPI(title="Dharma Debt Nexus API")
from src.models import DharmaGCN

# 1. Load the "Brain" on startup
# We rebuild the architecture and load the weights
INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM = 3, 16, 2
model = DharmaGCN(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)

# Path to the weights we just trained
model.load_state_dict(torch.load('models/dharma_weights.pth', weights_only=True))
model.eval()

# 2. Define the Request Schema
class BorrowerRequest(BaseModel):
    age: float
    income: float
    dharma_score: float

@app.post("/predict")
async def predict_risk(borrower: BorrowerRequest):
    # Convert incoming JSON to a tensor
    input_tensor = torch.tensor([[borrower.age, borrower.income, borrower.dharma_score]], dtype=torch.float)
    
    # In a real GNN, we'd need the edge_index for the full graph.
    # For a single prediction, we simulate a self-loop
    dummy_edge_index = torch.tensor([[0], [0]], dtype=torch.long)
    
    with torch.no_grad():
        # Pass through the GCN layers
        output = model.forward_as_single_node(input_tensor, dummy_edge_index) 
        prediction = torch.exp(output).argmax(dim=1).item()
    
    risk_status = "High Risk (Default)" if prediction == 1 else "Safe (Recoverable)"
    return {"status": "success", "prediction": risk_status}