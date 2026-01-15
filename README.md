# Dharma-Debt Nexus: GNN-Powered Debt Recovery Prediction

An end-to-end Machine Learning pipeline using **Graph Neural Networks (GCN)** to predict financial default risk in interconnected borrower networks.

## 🚀 Key Features
- **Relational Risk Modeling:** Uses GNNs to capture "financial contagion" where a borrower's risk is influenced by their connections.
- **PyTorch Geometric Core:** Implements a 2-layer Graph Convolutional Network (GCN) for node classification.
- **FastAPI Deployment:** Production-ready API for real-time risk inference.
- **Synthetic Graph Generation:** Rule-based generation of 1,000+ nodes simulating Indian Fintech credit clusters.

## 🛠️ Tech Stack
- **AI/ML:** PyTorch, PyTorch Geometric, Scikit-learn
- **API/Backend:** FastAPI, Uvicorn, Pydantic
- **Data:** Pandas, NumPy

## 📁 Project Structure
- `src/`: Core logic (GNN architecture & training loop)
- `api/`: FastAPI server implementation
- `data/`: Graph data generation and storage
- `models/`: Trained model weights (`.pth`)

## 🚦 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Generate data & train: `python src/trainer.py`
3. Launch API: `python -m uvicorn api.main:app --reload`