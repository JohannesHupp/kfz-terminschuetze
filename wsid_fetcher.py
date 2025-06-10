"""
wsid_fetcher.py

Modul zum Abrufen der aktuellen WSID (Session-ID) für die Terminbuchung.

Funktion:
- Sendet eine Anfrage an die BASE_URL.
- Liest die WSID aus dem HTTP-Redirect-Header ("Location") aus.

Wird genutzt in:
- main.py für die zyklische Erneuerung der Sitzung.

Besonderheiten:
- Automatisches Retry bei Verbindungsfehlern über den @retry-Decorator (utils.py).
"""

import re
import logging
import requests

from utils import retry
from config import BASE_URL

@retry(times=3, delay=2)
def fetch_wsid(uid: str, lang: str = "de") -> str:
    """
    Holt die aktuelle WSID (Session-ID) für die Buchung.

    Args:
        uid (str): Benutzer-ID (User Identifier) für die Terminseite.
        lang (str, optional): Spracheinstellung der Website (Standard: "de").

    Returns:
        str: Die extrahierte WSID.

    Raises:
        RuntimeError: Falls keine WSID im Redirect-Header gefunden wird.
    """
    params = {"uid": uid, "lang": lang}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1"}
    resp = requests.get(BASE_URL, params=params, headers=headers, allow_redirects=False)

    # Erwarteter Redirect-Statuscode prüfen
    if resp.status_code not in (301, 302):
        logging.warning(f"Unerwarteter HTTP-Statuscode {resp.status_code} beim WSID-Abruf.")

    # Redirect-URL auslesen und WSID extrahieren
    location = resp.headers.get("Location", "")
    match = re.search(r"wsid=([0-9a-fA-F\-]+)", location)
    if not match:
        raise RuntimeError("❌ Keine WSID im Location-Header gefunden!")

    return match.group(1)
