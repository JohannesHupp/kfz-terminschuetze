"""
wsid_fetcher.py

Ermittelt die aktuelle WSID per HTTP-Redirect-Header und liefert sie zurück.
"""

import re
import logging

import requests
from utils import retry
from config import BASE_URL

@retry(times=3, delay=2)
def fetch_wsid(uid: str, lang: str = "de") -> str:
    """
    Holt die aktuelle WSID, indem es die Basis-URL ohne Redirect folgt und
    den Location-Header ausliest.

    :param uid: Die eindeutige User-ID für die Terminbuchung
    :param lang: Sprachparameter (z.B. 'de')
    :return: WSID als String
    """
    params = {"uid": uid, "lang": lang}
    resp = requests.get(BASE_URL, params=params, allow_redirects=False)
    if resp.status_code not in (301, 302):
        logging.warning(f"Unerwarteter Statuscode {resp.status_code} beim WSID-Abruf")
    location = resp.headers.get("Location", "")
    match = re.search(r"wsid=([0-9a-fA-F\-]+)", location)
    if not match:
        raise RuntimeError("Keine wsid im Location-Header gefunden!")
    return match.group(1)
