# Prompt 5: Scheduler-Integration & Worker-Prozess

**Ziel:**  
Integriere einen Scheduler, der gemäß den Konfigurationen die Datenabrufe und Verarbeitungen automatisch ausführt.

**Anweisungen:**

- Nutze APScheduler in Kombination mit FastAPI, um Jobs zu planen.
- Erstelle Jobs, die:
  - Zu einer definierten Startzeit und Frequenz die Datenquellen abrufen.
  - Den entsprechenden Datenhandler-Skript auf die abgerufenen Daten anwenden.
  - Die verarbeiteten Daten in den konfigurierten Ausgabe-Pfad schreiben.
- Implementiere Fehlerbehandlung und Retry-Mechanismen für Abruf- oder Verarbeitungsfehler.