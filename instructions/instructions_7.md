# Prompt 7: Deployment & Docker Compose Konfiguration

**Ziel:**  
Erstelle eine Docker Compose-Konfiguration, die alle Komponenten (FastAPI-Backend, Scheduler (falls separat), Nginx als Reverse Proxy und HTTPS-Server) orchestriert.

**Anweisungen:**

- Erstelle ein `docker-compose.yml`-File, das Container für:
  - FastAPI (Backend und Scheduler)
  - Nginx (für HTTPS und statische Dateiauslieferung)
- Konfiguriere notwendige Volumes (z. B. für persistente Datenbankdateien und das Ausgabe-Verzeichnis).
- Dokumentiere im README die Schritte zum Deployment und die benötigten Umgebungsvariablen.
- Stelle sicher, dass der Nginx-Container als Reverse Proxy fungiert und Anfragen an das FastAPI-Backend weiterleitet.