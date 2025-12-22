FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Installation des packages Python incluant ddtrace
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt ddtrace

COPY . .

EXPOSE 5000

# Commande de lancement avec l'instrumentation Datadog
CMD ["ddtrace-run", "python", "app/main.py"]