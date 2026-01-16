# Use a full Python image instead of slim to ensure all build tools are present
FROM python:3.11

WORKDIR /app

# Ensure pip is up to date
RUN pip install --upgrade pip

# Copy requirements first
COPY requirements.txt .

# Install Torch and specific GNN dependencies before the rest
# This prevents the most common 'exit code: 1' errors
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-2.0.0+cpu.html

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Match Render's Port
EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]