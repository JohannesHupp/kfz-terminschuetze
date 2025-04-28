"""
main.py

Koordiniert den Terminbot: holt die aktuelle WSID, führt den Termin-Check durch
und pausiert zufällig zwischen den Durchläufen. Sendet eine E-Mail-Benachrichtigung
bei erfolgreicher Buchung und beendet sich danach.
"""
import logging
import sys

import config
from wsid_fetcher import fetch_wsid
from booking import run_booking_cycle
from utils import sleep_random
from notifier import send_notification_email


def main():
    # Logging in Datei und Konsole
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("terminbot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("🔔 Terminbot gestartet 🔔")

    while True:
        logging.info("--- Neuer Durchlauf ---")
        try:
            # WSID erneuern
            wsid = fetch_wsid(config.UID, config.LANG)
            logging.info(f"⭐ Angeforderte neue WSID: {wsid}")

            # Terminbuchungs-Flow ausführen
            gebucht = run_booking_cycle(wsid, submit=config.SUBMIT, debug=config.DEBUG)
            if gebucht:
                logging.info("✅ Ein Termin wurde erfolgreich gebucht.")
                # E-Mail-Benachrichtigung versenden
                if config.SEND_NOTIFICATION_EMAIL:
                    send_notification_email()
                    
                logging.info("Programm beendet sich.")
                sys.exit(0)

        except Exception as e:
            logging.exception(f"❌ Unerwarteter Fehler im Durchlauf: {e}")

        # Zufällige Pause zwischen den Checks
        sleep_random(config.MIN_WAIT_SECONDS, config.MAX_WAIT_SECONDS)


if __name__ == "__main__":
    main()