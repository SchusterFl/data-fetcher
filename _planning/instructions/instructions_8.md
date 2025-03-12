# Prompt 8: Logging, Monitoring & Health Checks

**Ziel:**  
Implementiere ein zentrales Logging, Health-Check Endpunkte und ggf. ein einfaches Monitoring für alle Module.

**Anweisungen:**

- Implementiere Logging-Middleware in FastAPI, die alle API-Aufrufe, Scheduler-Jobs und Fehler protokolliert.
- Erstelle Health-Check Endpunkte, die den Status der verschiedenen Module (API, Scheduler, Datenhandler) abfragen.
- Dokumentiere, wie Logs ausgewertet und ggf. in ein Dashboard integriert werden können (z. B. mit externen Monitoring-Tools).