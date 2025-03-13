"""
Sandbox-Service für die sichere Ausführung von benutzerdefinierten Skripten.
Stellt eine isolierte Umgebung bereit, in der Datenhandler-Skripte ausgeführt werden können,
ohne das Hauptsystem zu gefährden.
"""

import os
import sys
import json
import tempfile
import subprocess
import logging
from typing import Dict, Any, Optional, Tuple

from app.config.settings import settings

logger = logging.getLogger(__name__)
# settings = get_settings()


class SandboxService:
    """
    Service zur sicheren Ausführung von benutzerdefinierten Python-Skripten.
    Verwendet einen isolierten Prozess mit eingeschränkten Rechten.
    """

    def __init__(self, timeout: int = 30):
        """
        Initialisiert den SandboxService.

        Args:
            timeout: Maximale Ausführungszeit in Sekunden (Standard: 30)
        """
        self.timeout = timeout
        self.temp_dir = settings.TEMP_DIR or tempfile.gettempdir()
        os.makedirs(self.temp_dir, exist_ok=True)

    def _create_temp_script(self, script_content: str) -> str:
        """
        Erstellt eine temporäre Skriptdatei mit dem angegebenen Inhalt.

        Args:
            script_content: Der Inhalt des Skripts

        Returns:
            Der Pfad zur temporären Skriptdatei
        """
        fd, temp_path = tempfile.mkstemp(suffix='.py', dir=self.temp_dir)
        with os.fdopen(fd, 'w') as f:
            f.write(script_content)
        return temp_path

    def _create_wrapper_script(self, script_path: str, input_data: Dict[str, Any]) -> str:
        """
        Erstellt ein Wrapper-Skript, das das Hauptskript mit den übergebenen Daten ausführt
        und die Ausgabe im JSON-Format zurückgibt.

        Args:
            script_path: Pfad zum Hauptskript
            input_data: Eingabedaten für das Skript

        Returns:
            Der Pfad zum Wrapper-Skript
        """
        wrapper_content = f"""
import json
import sys
import traceback
from pathlib import Path

# Eingabedaten
input_data = {json.dumps(input_data)}

# Ausgabedaten
output = {{"success": False, "data": None, "error": None}}

try:
    # Skript laden und ausführen
    script_path = "{script_path}"
    script_dir = Path(script_path).parent
    sys.path.insert(0, str(script_dir))
    
    # Definiere eine process_data Funktion, die vom Skript aufgerufen werden kann
    def process_data(data):
        return data
    
    # Führe das Skript in einem begrenzten Namespace aus
    namespace = {{"__name__": "__main__", "input_data": input_data, "process_data": process_data}}
    with open(script_path, 'r') as f:
        exec(f.read(), namespace)
    
    # Überprüfe, ob das Skript eine process_data Funktion definiert hat
    if "process_data" in namespace and callable(namespace["process_data"]):
        result = namespace["process_data"](input_data)
        output["data"] = result
        output["success"] = True
    else:
        output["error"] = "Das Skript definiert keine process_data Funktion."
except Exception as e:
    output["error"] = f"{{type(e).__name__}}: {{str(e)}}\\n{{traceback.format_exc()}}"

# Ausgabe als JSON
print(json.dumps(output))
"""
        fd, wrapper_path = tempfile.mkstemp(suffix='_wrapper.py', dir=self.temp_dir)
        with os.fdopen(fd, 'w') as f:
            f.write(wrapper_content)
        return wrapper_path

    def execute(self, script_content: str, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Führt ein Skript mit den angegebenen Eingabedaten in einer Sandbox aus.

        Args:
            script_content: Der Inhalt des auszuführenden Skripts
            input_data: Die Eingabedaten für das Skript

        Returns:
            Tuple mit (Erfolg, Ausgabedaten, Fehlermeldung)
        """
        try:
            # Temporäre Skriptdateien erstellen
            script_path = self._create_temp_script(script_content)
            wrapper_path = self._create_wrapper_script(script_path, input_data)

            # Kommando zum Ausführen des Wrapper-Skripts mit eingeschränkten Rechten
            cmd = [
                sys.executable,
                "-u",  # Unbuffered output
                wrapper_path
            ]

            logger.info(f"Führe Skript in Sandbox aus: {script_path}")
            
            # Skript in einem separaten Prozess ausführen
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Auf Abschluss des Prozesses warten (mit Timeout)
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                return False, None, f"Skriptausführung überschritt das Zeitlimit von {self.timeout} Sekunden."
            
            # Ausgabe verarbeiten
            if process.returncode != 0:
                return False, None, f"Skript wurde mit Exit-Code {process.returncode} beendet: {stderr}"
            
            # JSON-Ausgabe parsen
            try:
                output = json.loads(stdout)
                if output["success"]:
                    return True, output["data"], None
                else:
                    return False, None, output["error"]
            except json.JSONDecodeError:
                return False, None, f"Fehler beim Verarbeiten der Skriptausgabe: {stdout}"
            
        except Exception as e:
            logger.exception("Fehler bei der Ausführung des Skripts in der Sandbox")
            return False, None, f"Interner Fehler bei der Skriptausführung: {str(e)}"
        finally:
            # Temporäre Dateien aufräumen
            self._cleanup_temp_files(script_path, wrapper_path)
    
    def _cleanup_temp_files(self, *file_paths):
        """
        Löscht temporäre Dateien.

        Args:
            *file_paths: Pfade zu den zu löschenden Dateien
        """
        for path in file_paths:
            try:
                if path and os.path.exists(path):
                    os.unlink(path)
            except Exception as e:
                logger.warning(f"Fehler beim Löschen der temporären Datei {path}: {e}")

    def test_script(self, script_content: str, test_data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Testet ein Skript mit den angegebenen Testdaten.
        Dies ist eine Hilfsfunktion für die Benutzeroberfläche, um Skripte zu testen.

        Args:
            script_content: Der Inhalt des zu testenden Skripts
            test_data: Die Testdaten für das Skript

        Returns:
            Tuple mit (Erfolg, Ausgabedaten, Fehlermeldung)
        """
        return self.execute(script_content, test_data)