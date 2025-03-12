"""
Validierungsfunktionen für die Data Fetch & Process Webapp.
Stellt Funktionen zur Validierung von URLs, Zeitplänen und anderen Daten bereit.
"""

import re
import json
import logging
from typing import Union, Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse
import requests
from datetime import datetime, timedelta
from croniter import croniter

logger = logging.getLogger(__name__)


def validate_url(url: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Überprüft, ob eine URL gültig ist und ob sie erreichbar ist.

    Args:
        url: Die zu validierende URL
        timeout: Timeout für die Anfrage in Sekunden

    Returns:
        Tuple mit (ist_gültig, Fehlermeldung oder None)
    """
    # Grundlegende URL-Struktur überprüfen
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "URL ist unvollständig (Schema oder Host fehlt)"
        
        # Sicherstellen, dass nur HTTP(S) verwendet wird
        if result.scheme not in ['http', 'https']:
            return False, "Nur HTTP und HTTPS URLs werden unterstützt"
    except Exception as e:
        return False, f"Ungültige URL-Struktur: {str(e)}"
    
    # Optional: Erreichbarkeit der URL testen
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400:
            return False, f"URL ist nicht erreichbar (Status-Code: {response.status_code})"
    except requests.RequestException as e:
        return False, f"Fehler beim Zugriff auf die URL: {str(e)}"
    
    return True, None


def validate_schedule(schedule: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Überprüft, ob ein geplanter Zeitplan gültig ist.
    Unterstützt 'cron' und 'interval' Typen.

    Args:
        schedule: Ein Dictionary mit den Zeitplan-Informationen
            Für 'cron': {'type': 'cron', 'expression': '* * * * *'}
            Für 'interval': {'type': 'interval', 'minutes': 30}

    Returns:
        Tuple mit (ist_gültig, Fehlermeldung oder None)
    """
    if 'type' not in schedule:
        return False, "Zeitplantyp fehlt"
    
    schedule_type = schedule['type']
    
    if schedule_type == 'cron':
        # Cron-Expression validieren
        if 'expression' not in schedule:
            return False, "Cron-Expression fehlt"
        
        try:
            # Überprüfen, ob die Cron-Expression gültig ist
            if not croniter.is_valid(schedule['expression']):
                return False, "Ungültige Cron-Expression"
        except Exception as e:
            return False, f"Fehler bei der Validierung der Cron-Expression: {str(e)}"
            
    elif schedule_type == 'interval':
        # Intervall validieren
        if 'minutes' not in schedule:
            return False, "Intervall in Minuten fehlt"
        
        try:
            minutes = int(schedule['minutes'])
            if minutes <= 0:
                return False, "Intervall muss größer als 0 sein"
        except (ValueError, TypeError):
            return False, "Intervall muss eine positive Ganzzahl sein"
            
    else:
        return False, f"Unbekannter Zeitplantyp: {schedule_type}"
    
    return True, None


def validate_script(script_content: str) -> Tuple[bool, Optional[str]]:
    """
    Überprüft, ob ein Python-Skript grundlegend syntaktisch korrekt ist.
    Prüft auch auf verbotene Importe und Funktionen.

    Args:
        script_content: Der Inhalt des zu validierenden Skripts

    Returns:
        Tuple mit (ist_gültig, Fehlermeldung oder None)
    """
    # Liste von verbotenen Modulen/Funktionen
    forbidden_imports = [
        'os', 'subprocess', 'sys', 'shutil', 'socket', 'requests',
        '__import__', 'eval', 'exec', 'compile', 'open', 'file'
    ]
    
    # Nach verbotenen Importen suchen
    for module in forbidden_imports:
        pattern = rf'(^|\W)(import\s+{module}|from\s+{module}\s+import|__import__\([\'"]?{module}|eval\(|exec\(|compile\()'
        if re.search(pattern, script_content, re.MULTILINE):
            return False, f"Das Skript enthält nicht erlaubte Funktionen oder Importe: {module}"
    
    # Syntaxprüfung
    try:
        compile(script_content, '<string>', 'exec')
    except SyntaxError as e:
        return False, f"Syntaxfehler im Skript: {str(e)}"
    
    # Überprüfen, ob das Skript eine process_data-Funktion enthält
    if not re.search(r'def\s+process_data\s*\(', script_content):
        return False, "Das Skript muss eine process_data Funktion definieren"
    
    return True, None


def validate_output_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    Überprüft, ob ein Ausgabepfad gültig ist.
    Der Pfad sollte relativ zum Ausgabeverzeichnis sein und darf keine
    gefährlichen Pfadbestandteile enthalten.

    Args:
        path: Der zu validierende Pfad

    Returns:
        Tuple mit (ist_gültig, Fehlermeldung oder None)
    """
    # Überprüfen auf absolute Pfade oder Path-Traversal-Versuche
    if path.startswith('/') or path.startswith('\\'):
        return False, "Absolute Pfade sind nicht erlaubt"
    
    # Auf Path-Traversal-Versuch prüfen
    if '..' in path.split('/') or '..' in path.split('\\'):
        return False, "Der Pfad darf keine übergeordneten Verzeichnisreferenzen (..) enthalten"
    
     # Auf ungültige Zeichen prüfen
    forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in path for char in forbidden_chars):
        return False, f"Der Pfad enthält ungültige Zeichen: {forbidden_chars}"
    
    # Optional: Sicherstellen, dass der Pfad nicht auf ein Verzeichnis zeigt
    if path.endswith(path.sep):
        return False, "Der Pfad darf nicht auf ein Verzeichnis enden"

    return True, None