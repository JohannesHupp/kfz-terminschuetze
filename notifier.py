"""
notifier.py

Modul zur Versendung einer E-Mail-Benachrichtigung bei erfolgreicher Terminbuchung.

Aufgaben:
- Baut eine SMTP-Verbindung auf.
- Sendet eine formatierte E-Mail an den definierten Empfänger.
- Handhabt und loggt mögliche Fehler beim E-Mail-Versand.

Verwendet:
- Konfigurationsdaten aus config.py (SMTP-Server, Absender, Empfänger, Zugangsdaten).
"""

import logging
import smtplib
from email.mime.text import MIMEText

import config

import http.client
import urllib

def send_notification_email():
    """
    Sendet eine Benachrichtigungs-E-Mail nach erfolgreicher Terminbuchung.
    Die E-Mail enthält einen kurzen Hinweistext.
    """
    subject = "🎉 Termin erfolgreich gebucht!"
    body = (
        "Eure Majestät, der Termin wurde erfolgreich gebucht.\n"
        "Weitere Details entnehmt bitte dem Protokoll."
    )

    # Erzeuge die E-Mail-Nachricht
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.ABSENDER
    msg["To"] = config.EMPFAENGER

    try:
        # SMTP-Server verbinden und E-Mail senden
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
            smtp.starttls()  # Sichere Verbindung aufbauen
            smtp.login(config.SMTP_USER, config.SMTP_PASS)  # Authentifizieren
            smtp.send_message(msg)  # E-Mail absenden
        logging.info("📧 Benachrichtigungs-E-Mail erfolgreich gesendet.")
    except Exception as e:
        # Fehler beim Senden der E-Mail protokollieren
        logging.error(f"❌ Fehler beim Senden der Benachrichtigungs-E-Mail: {e}")

def send_pushover_notification():
    """
    Sendet eine Push-Benachrichtigung über Pushover.
    """
    try:
        conn = http.client.HTTPSConnection("api.pushover.net", 443)
        payload = urllib.parse.urlencode({
            "token": config.PUSHOVER_APP_TOKEN,
            "user": config.PUSHOVER_USER_KEY,
            "title": "🎉 Termin erfolgreich gebucht!",
            "message": ("Eure Majestät, der Termin wurde erfolgreich gebucht.\n"
                        "Weitere Details entnehmt bitte dem Protokoll.")
        })
        headers = { "Content-type": "application/x-www-form-urlencoded" }

        conn.request("POST", "/1/messages.json", payload, headers)
        response = conn.getresponse()

        if response.status == 200:
            logging.info("✅ Pushover-Benachrichtigung erfolgreich gesendet.")
        else:
            logging.warning(f"⚠️ Fehler beim Senden der Pushover-Benachrichtigung: "
                            f"{response.status} {response.reason}")

        conn.close()

    except Exception as e:
        logging.error(f"❌ Fehler beim Senden der Pushover-Benachrichtigung: {e}")
