FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download SPECTER model so it's baked into the image
# (avoids slow cold-start downloads on every restart)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('allenai-specter')"

# Copy backend source and data
COPY backend/ .

# HuggingFace Spaces requires port 7860
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
