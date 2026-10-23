FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
