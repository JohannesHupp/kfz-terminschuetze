"""
main.py

Hauptmodul des KFZ Terminbots.

Aufgaben:
- Startet den Bot und initialisiert das Logging.
- Fordert eine neue WSID (Session-ID) an.
- Versucht, einen Termin zu buchen.
- Versendet bei erfolgreicher Buchung eine E-Mail-Benachrichtigung.
- Wartet zufällig zwischen den Buchungsversuchen.
- Beendet sich nach erfolgreicher Buchung automatisch.

Weitere Module:
- wsid_fetcher.py: Holt die aktuelle WSID.
- booking.py: Führt den Buchungsprozess durch.
- utils.py: Stellt Hilfsfunktionen bereit (z.B. zufällige Pausen).
- notifier.py: Versendet E-Mail-Benachrichtigungen.
"""

import logging
import sys

import config
from wsid_fetcher import fetch_wsid
from booking import run_booking_cycle
from utils import sleep_random
from notifier import send_notification_email

def main():
    """
    Hauptfunktion des Terminbots.
    Koordiniert die wiederholte Terminprüfung und Buchung.
    """
    # Initialisiere Logging in Datei und Konsole
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

    # Endlosschleife: Immer wieder nach Terminen suchen
    while True:
        logging.info("--- Neuer Durchlauf gestartet ---")
        try:
            # 1. WSID (Session-ID) erneuern
            wsid = fetch_wsid(config.UID, config.LANG)
            logging.info(f"⭐ Neue WSID erhalten: {wsid}")

            # 2. Buchungsversuch mit aktueller WSID
            gebucht = run_booking_cycle(wsid, submit=config.SUBMIT, debug=config.DEBUG)
            if gebucht:
                logging.info("✅ Termin wurde erfolgreich gebucht.")

                # 3. Optional: E-Mail-Benachrichtigung bei erfolgreicher Buchung
                if config.SEND_NOTIFICATION_EMAIL:
                    send_notification_email()

                # 4. Erfolgreiche Buchung -> Programm beenden
                logging.info("🏁 Terminbuchung abgeschlossen. Programm wird beendet.")
                sys.exit(0)

        except Exception as e:
            # Fehlerprotokollierung für Debugging
            logging.exception(f"❌ Unerwarteter Fehler während des Durchlaufs: {e}")

        # 5. Zufällige Pause zwischen den Versuchen
        sleep_random(config.MIN_WAIT_SECONDS, config.MAX_WAIT_SECONDS)


# Starte den Bot, wenn dieses Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()
