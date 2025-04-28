"""
notifier.py

Kapselt die E-Mail-Benachrichtigung für erfolgreiche Buchungen.
"""

import logging
import smtplib
from email.mime.text import MIMEText

import config

def send_notification_email():
    """
    Sendet eine E-Mail-Benachrichtigung, dass ein Termin erfolgreich gebucht wurde.
    """
    subject = "🎉 Termin erfolgreich gebucht!"
    body = (
        f"Eure Majestät, der Termin wurde erfolgreich gebucht.\n"
        f"Weitere Details entnehmt bitte dem Protokoll."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.ABSENDER
    msg["To"] = config.EMPFAENGER

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config.SMTP_USER, config.SMTP_PASS)
            smtp.send_message(msg)
        logging.info("📧 Benachrichtigungs-E-Mail gesendet.")
    except Exception as e:
        logging.error(f"❌ Fehler beim Senden der E-Mail-Benachrichtigung: {e}")
