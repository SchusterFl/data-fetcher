# Data Fetcher

## Prompt 1: Projekt-Setup & Grundstruktur

**Ziel:**  
Erstelle ein Basisprojekt mit FastAPI, SQLite und einer sinnvollen Ordnerstruktur, die später die Module (API, Scheduler, Datenmodelle, etc.) unterteilt.

**Anweisungen:**

- Erstelle ein neues FastAPI-Projekt.
- Richte SQLite als Datenbank ein.
- Definiere eine Ordnerstruktur (z. B. `app/api`, `app/models`, `app/scheduler`, `app/config`, `app/utils`).
- Erstelle eine Grundkonfiguration (z. B. für Logging, Umgebungsvariablen) und initiale API-Routen (z. B. `/health` als Health-Check).
- Dokumentiere die Projektstruktur in einem README.

**Anhänge:**  
Füge einen Auszug aus dem Konzept (Abschnitt „Gesamtkonzept: Data Fetch & Process Webapp – Architektur & Komponenten: Backend (FastAPI + SQLite)“) bei, damit der Kontext zur Persistenz und API-Grundlagen klar ist.

## Prompt 2: API-Endpunkte für Datenquellen-Management

**Ziel:**  
Implementiere CRUD-API-Endpunkte, die Datenquellen verwalten (URL, Startzeit, Frequenz etc.).

**Anweisungen:**

- Entwickle API-Routen für das Erstellen, Lesen, Aktualisieren und Löschen von Datenquellen.
- Implementiere eine Validierung für die URL (Sicherstellen, dass der angegebene HTTP/HTTPS-Endpunkt erreichbar ist).
- Speichere und lese Konfigurationen aus der SQLite-Datenbank.
- Integriere Fehlerbehandlung und Logging (z. B. für fehlgeschlagene Abrufe oder ungültige Eingaben).

**Anhänge:**  
Beziehe dich auf den Abschnitt „3.1. Datenquellen-Management“ aus dem Konzept, um Details zur Validierung und Fehlerbehandlung zu übermitteln.

## Prompt 3: Modul für Datenhandler-Verwaltung

**Ziel:**  
Erstelle API-Endpunkte und ein Datenmodell zur Verwaltung benutzerdefinierter Skripte (Datenhandler).

**Anweisungen:**

- Definiere ein Datenmodell für Datenhandler (Felder wie Name, Skriptinhalt, Version, Erstellungsdatum).
- Implementiere CRUD-Endpunkte, um Skripte zu erstellen, zu bearbeiten, zu testen und zu löschen.
- Integriere einen „Testmodus“, in dem Beispiel-Daten an das Skript übergeben werden, um dessen Ausgabe zu validieren.
- Skizziere ein Konzept zur Sandbox-Ausführung der Skripte (z. B. Ausführung in isolierten Prozessen).

**Anhänge:**  
Füge den Abschnitt „3.2. Datenhandler“ aus dem Konzept bei, um Anforderungen an Testumgebung, Versionierung und Sandbox zu veranschaulichen.

## Prompt 4: Modul für Ausgabe-Pfade & Dateimanagement

**Ziel:**  
Implementiere die Konfiguration der Ausgabeorte, inklusive Optionen zum Überschreiben oder zum Erzeugen neuer Dateien mit Zeitstempel sowie einen Deletion-Service.

**Anweisungen:**

- Entwickle API-Endpunkte für das Erstellen und Verwalten von Ausgabe-Pfaden.
- Implementiere Optionen, um entweder eine Datei zu überschreiben oder neue Dateien mit einem modifizierbaren Zeitstempel anzulegen.
- Entwickle einen Hintergrundjob (über APScheduler), der alte Dateien in einem definierten Intervall löscht.
- Stelle sicher, dass Schreibvorgänge atomar und fehlertolerant sind.

**Anhänge:**  
Verweise auf den Abschnitt „3.3. Ausgabe-Pfade & Dateimanagement“ aus dem Konzept, um die Anforderungen an Dateispeicherung und den Deletion-Service klarzustellen.

## Prompt 5: Scheduler-Integration & Worker-Prozess

**Ziel:**  
Integriere einen Scheduler, der gemäß den Konfigurationen die Datenabrufe und Verarbeitungen automatisch ausführt.

**Anweisungen:**

- Nutze APScheduler in Kombination mit FastAPI, um Jobs zu planen.
- Erstelle Jobs, die:
  - Zu einer definierten Startzeit und Frequenz die Datenquellen abrufen.
  - Den entsprechenden Datenhandler-Skript auf die abgerufenen Daten anwenden.
  - Die verarbeiteten Daten in den konfigurierten Ausgabe-Pfad schreiben.
- Implementiere Fehlerbehandlung und Retry-Mechanismen für Abruf- oder Verarbeitungsfehler.

**Anhänge:**  
Füge den Abschnitt „2. Architektur & Komponenten – Scheduler & Worker“ aus dem Konzept bei, um den Ablauf der geplanten Tasks zu verdeutlichen.

## Prompt 6: Frontend-Entwicklung mit Vue.js

**Ziel:**  
Erstelle ein Frontend-Dashboard in Vue.js, das alle Konfigurationsmodule (Datenquellen, Datenhandler, Ausgabe-Pfade) integriert und mit den FastAPI-Endpunkten kommuniziert.

**Anweisungen:**

- Starte ein neues Vue.js-Projekt und richte die grundlegende Projektstruktur ein.
- Implementiere Views/Komponenten:
  - **Datenquellen-View:** Formular zur Eingabe von URL, Startzeit und Frequenz.
  - **Datenhandler-View:** Editor zum Erstellen, Testen und Verwalten von Skripten.
  - **Ausgabe-Pfad-View:** Formular zur Auswahl des Ausgabeortes und der Speicheroptionen.
- Sorge für eine konsistente REST-API-Anbindung zu den Backend-Endpunkten.
- Implementiere eine Benutzeroberfläche zur Anzeige von Logs oder Fehlermeldungen.

**Anhänge:**  
Beziehe den Abschnitt „2. Frontend (Vue.js)“ aus dem Konzept ein, um das gewünschte Dashboard und die Modulstruktur zu verdeutlichen.

## Prompt 7: Deployment & Docker Compose Konfiguration

**Ziel:**  
Erstelle eine Docker Compose-Konfiguration, die alle Komponenten (FastAPI-Backend, Scheduler (falls separat), Nginx als Reverse Proxy und HTTPS-Server) orchestriert.

**Anweisungen:**

- Erstelle ein `docker-compose.yml`-File, das Container für:
  - FastAPI (Backend und Scheduler)
  - Nginx (für HTTPS und statische Dateiauslieferung)
- Konfiguriere notwendige Volumes (z. B. für persistente Datenbankdateien und das Ausgabe-Verzeichnis).
- Dokumentiere im README die Schritte zum Deployment und die benötigten Umgebungsvariablen.
- Stelle sicher, dass der Nginx-Container als Reverse Proxy fungiert und Anfragen an das FastAPI-Backend weiterleitet.

**Anhänge:**  
Füge den Abschnitt „3.5. Deployment & Umgebung“ aus dem Konzept bei, um den Kontext der Container-Orchestrierung klarzumachen.

## Prompt 8: Logging, Monitoring & Health Checks

**Ziel:**  
Implementiere ein zentrales Logging, Health-Check Endpunkte und ggf. ein einfaches Monitoring für alle Module.

**Anweisungen:**

- Implementiere Logging-Middleware in FastAPI, die alle API-Aufrufe, Scheduler-Jobs und Fehler protokolliert.
- Erstelle Health-Check Endpunkte, die den Status der verschiedenen Module (API, Scheduler, Datenhandler) abfragen.
- Dokumentiere, wie Logs ausgewertet und ggf. in ein Dashboard integriert werden können (z. B. mit externen Monitoring-Tools).

**Anhänge:**  
Verweise auf den Abschnitt „3.4. Logging & Monitoring“ aus dem Konzept, um die Anforderungen an das Monitoring und die Health Checks zu verdeutlichen.
