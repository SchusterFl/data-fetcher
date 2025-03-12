# Concept

## Gesamtkonzept: Data Fetch & Process Webapp

### 1. Überblick und Ziele

**Ziel:**  

Entwicklung einer internen Webapplikation, mit der Benutzer:

- **Datenquellen** (über HTTP/HTTPS abrufbare Dateien) konfigurieren können (inklusive Startzeit und Abruffrequenz).
- **Datenhandler** konfigurieren und verwalten können, die per Skript die abgerufenen Daten modifizieren.
- **Ausgabepfade** definieren können, in die die verarbeiteten Daten geschrieben werden – entweder als Überschreibung einer bestehenden Datei oder als neue Datei mit Zeitstempel. Zusätzlich soll ein Deletion-Service alte Dateien nach einem definierten Intervall löschen.

**Modularität:**  
Die Lösung soll in drei klare Module unterteilt werden:

- **Datenquellen-Management**
- **Datenhandler-Verwaltung**
- **Daten-Ausgabe und Dateimanagement**

### 2. Architektur & Komponenten

#### A. Frontend (Vue.js)

- **Dashboard:**  
  Eine zentrale Oberfläche, über die der Nutzer:
  - Neue Datenquellen hinzufügen, bestehende editieren oder löschen kann.
  - Datenhandler-Skripte definieren, testen und verwalten kann.
  - Ausgabeziele konfigurieren kann (inklusive Auswahl der Speicherstrategie).
- **Module/Views:**
  - **Datenquellen-View:** Formulare zur Eingabe der URL, Startzeit, Frequenz und weiteren Parametern.
  - **Datenhandler-View:** Editor für Skripte mit Testfunktion (Inputbeispiele) und Fehlerausgabe.
  - **Ausgabe-Path-View:** Konfiguration der Speicherorte, Auswahl zwischen "Überschreiben" und "neue Datei mit Zeitstempel" sowie Einstellung für den Deletion-Service.
- **Kommunikation:**  
  Verwendung von REST-API-Endpunkten (über FastAPI) zur Synchronisation und Verwaltung der Daten.

#### B. Backend (FastAPI + SQLite)

- **REST API:**  
  Bereitstellung von Endpunkten für CRUD-Operationen zu den drei Modulen:
  - **Datenquellen:** Endpunkte zur Erstellung, Aktualisierung, Abfrage und Löschung von Datenquellen.
  - **Datenhandler:** Endpunkte zur Verwaltung von Skripten (Speichern, Testen, Versionierung).
  - **Ausgabe-Pfade:** Endpunkte für die Konfiguration der Speicherorte und deren Optionen.
- **Persistenz:**  
  Nutzung von SQLite zur Speicherung aller Konfigurationen, Logs und Statusinformationen. Hierdurch wird eine einfache, aber effektive persistente Datenhaltung gewährleistet.
- **Scheduler & Worker:**  
  - Einsatz eines Scheduling-Moduls (z. B. mittels APScheduler) zur Verwaltung der geplanten Abrufe:
    - Initialer Abruf zur definierten Startzeit.
    - Wiederkehrende Abrufe basierend auf der eingestellten Frequenz.
  - Ausführung der definierten Datenhandler-Skripte in einem sicheren, isolierten Kontext.
- **Sandbox für Datenhandler:**  
  - Die Skripte der Nutzer sollen in einer abgesicherten Umgebung laufen, um Missbrauch zu vermeiden. Hier sollte ein Konzept zur Sandbox-Einbindung (z. B. isolierte Prozesse oder eingeschränkte Ausführungsumgebungen) entwickelt werden.
  - Fehler- und Exception-Handling muss eingebaut werden, damit bei fehlerhaften Skripten der Ablauf nicht unterbrochen wird.

#### C. Output Server (Nginx)

- **Reverse Proxy & HTTPS:**  
  - Nginx dient als Reverse Proxy, um Anfragen an die FastAPI weiterzuleiten.
  - Nginx konfiguriert auch HTTPS zur sicheren Bereitstellung der gespeicherten Dateien.
- **Statische Dateiauslieferung:**  
  - Konfiguration, dass das Output-Verzeichnis (welches von FastAPI befüllt wird) über Nginx erreichbar ist.
  - Einfache Konfiguration, die es ermöglicht, entweder immer dieselbe Datei zu überschreiben oder mit einem modifizierbaren Zeitstempel neue Dateien zu erstellen.

### 3. Detailaufgaben und Anforderungen

#### 3.1. Datenquellen-Management

- **Anforderungen:**
  - URL validieren und sicherstellen, dass die Quelle erreichbar ist.
  - Zeitpläne für den Abruf konfigurieren (Startzeit, Frequenz).
  - Fehlerbehandlung: Was passiert, wenn der Abruf fehlschlägt (Retry-Mechanismen, Logging)?
- **Aufgaben:**
  - REST-Endpunkte zur Verwaltung der Datenquellen.
  - Implementierung eines Validierungsmechanismus für URLs.
  - Logging der Abruf-Vorgänge und Fehlermeldungen.

#### 3.2. Datenhandler

- **Anforderungen:**
  - Erstellung, Speicherung und Versionierung von Skripten.
  - Testumgebung im Frontend, um Skripte auf Beispiel-Daten zu prüfen.
  - Sandbox-Umgebung zur sicheren Ausführung der Skripte.
- **Aufgaben:**
  - Design eines Datenmodells in der DB für Skripte (Name, Inhalt, Version, Erstellungsdatum).
  - API-Endpunkte für das Erstellen, Bearbeiten, Testen und Löschen der Skripte.
  - Konzept für die isolierte Ausführung (z. B. separater Prozess oder Container, falls möglich).

#### 3.3. Ausgabe-Pfade & Dateimanagement

- **Anforderungen:**
  - Konfiguration des Zielordners, in den die verarbeiteten Daten geschrieben werden.
  - Auswahl zwischen Dateiüberschreibung und Erzeugung neuer Dateien mit Zeitstempel.
  - Implementierung eines Jobs, der alte Dateien in einem definierten Intervall löscht.
- **Aufgaben:**
  - API-Endpunkte zur Verwaltung der Ausgabe-Konfiguration.
  - Sicherstellen, dass die Schreiboperationen atomar und fehlertolerant sind.
  - Integration eines Jobs im Scheduler für die periodische Löschung älterer Dateien.
  - Dokumentation der Konfigurationsoptionen und deren Auswirkungen.

#### 3.4. Logging & Monitoring

- **Anforderungen:**
  - Ausführliches Logging aller Abrufe, Skript-Ausführungen und Dateispeicherungen.
  - Health-Checks für die einzelnen Module (Backend, Scheduler, Output Server).
- **Aufgaben:**
  - Implementierung eines zentralen Logging-Mechanismus (z. B. über FastAPI-Middleware).
  - Entwicklung von Health-Check Endpunkten, die den Status des Systems abfragen.
  - Dokumentation und ggf. Einbindung eines einfachen Dashboards für den Überblick.

#### 3.5. Deployment & Umgebung

- **Anforderungen:**
  - Verwendung von Docker Compose zur Orchestrierung der Container.
  - Separate Container für FastAPI (Backend), Scheduler (falls getrennt) und Nginx.
- **Aufgaben:**
  - Erstellung eines Docker Compose-Files, das alle notwendigen Container definiert.
  - Dokumentation der Deployment-Schritte und der notwendigen Konfigurationen (z. B. Umgebungsvariablen, Volumes für persistente Daten).

### 4. Sicherheits- und Qualitätsaspekte

- **Sandboxing der Datenhandler:**  
  Eine der größten Herausforderungen ist die Ausführung benutzerdefinierter Skripte. Es muss sichergestellt werden, dass diese nicht auf das System zugreifen können. Ein Konzept zur sicheren Sandbox muss entwickelt und dokumentiert werden.

- **Fehlerbehandlung:**  
  Definierte Retry-Mechanismen und Fallback-Strategien sollten implementiert werden, sodass bei temporären Fehlern der Prozess nicht stoppt. Alle Fehler sollten ausführlich geloggt und im Frontend sichtbar gemacht werden.

- **Modularität & Erweiterbarkeit:**  
  Die Trennung der Module (Datenquellen, Datenhandler, Ausgabe) ermöglicht spätere Erweiterungen (z. B. Hinzufügen neuer Datenhandler oder weiterer Ausgabeoptionen) ohne grundlegende Änderungen an der Architektur.

- **Dokumentation:**  
  Jede Komponente sollte umfassend dokumentiert werden – von der API-Dokumentation (z. B. mittels OpenAPI/Swagger) bis hin zu Deployment-Anleitungen und Sicherheitskonzepten.
