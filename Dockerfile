# Verwende ein offizielles Python Runtime als Eltern-Image
FROM python:3.8

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die aktuellen Verzeichnisse in das Arbeitsverzeichnis
COPY . /app

# Installiere alle benötigten Pakete aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mache Port 5000 verfügbar für die Welt außerhalb dieses Containers
EXPOSE 5000

# Führe app.py beim Start des Containers aus
CMD ["python", "app.py"]
