FROM python:3.11-slim

WORKDIR /app/env


COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt


COPY models.py .
COPY tickets.py .
COPY __init__.py .
COPY openenv.yaml .
COPY server/__init__.py ./server/__init__.py
COPY server/app.py ./server/app.py
COPY server/triage_environment.py ./server/triage_environment.py


ENV PYTHONPATH=/app/env


ENV PORT=7860
EXPOSE 7860


ENV TRIAGE_TASK=easy_triage

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import requests; r=requests.get('http://localhost:7860/health'); assert r.status_code==200" || exit 1

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
