# Prompt 4: Modul für Ausgabe-Pfade & Dateimanagement

**Ziel:**  
Implementiere die Konfiguration der Ausgabeorte, inklusive Optionen zum Überschreiben oder zum Erzeugen neuer Dateien mit Zeitstempel sowie einen Deletion-Service.

**Anweisungen:**

- Entwickle API-Endpunkte für das Erstellen und Verwalten von Ausgabe-Pfaden.
- Implementiere Optionen, um entweder eine Datei zu überschreiben oder neue Dateien mit einem modifizierbaren Zeitstempel anzulegen.
- Entwickle einen Hintergrundjob (über APScheduler), der alte Dateien in einem definierten Intervall löscht.
- Stelle sicher, dass Schreibvorgänge atomar und fehlertolerant sind.