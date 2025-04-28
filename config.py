"""
config.py

Zentrale Konfigurationsdatei für den Terminbot.
Enthält technische Parameter, Ziel-Datum sowie persönliche Buchungsdaten.
"""

# ——————————————
# Technische Basis-Parameter
# ——————————————
UID           = "67523a04-37af-4131-9495-0a3566e0eb8b"                              # Sitzungsschlüssel
LANG          = "de"                                                                # Sprache der UI
BASE_URL      = "https://termine.stadt-koeln.de/m/kfz-zulassung/extern/calendar/"   # Basis URL der Seite
EC_TIMEOUT    = 15                                                                  # Sekunden für ExpectedConditions in Selenium
BOOKING_PATH  = "booking?"                                                          # Teilstring der URL für die Buchungsseite

# ——————————————
# Zielmonat und -tage für die Terminbuchung
# ——————————————
TARGET_MONTH  = 4            # Monatsnummer (z.B. 5 für Mai)
TARGET_DAYS   = [29]         # Liste der Tagesnummern (z.B. [21, 22, 23])

# ——————————————
# Warteintervalle
# ——————————————
MIN_WAIT_SECONDS = 30   # minimale Pause zwischen den Checks
MAX_WAIT_SECONDS = 90   # maximale Pause zwischen den Checks

# ——————————————
# Persönliche Buchungsdaten
# ——————————————
SALUTATION   = "Herr"       # Anrede (Herr/Frau)
FIRST_NAME   = "Max"
LAST_NAME    = "Mustermann"
EMAIL        = "Max.Mustermann@abc.de"
PHONE        = "0123456789"
FIN1         = "xxxxxxxxxxxxxxxxx"
FIN2         = ""           # optional
FIN3         = ""           # optional

# ——————————————
# Ablaufsteuerung
# ——————————————
SUBMIT                   = True          # True: Buchung abschicken; False: Dry-Run
DEBUG                    = False         # True: Browser-Fenster im Debug öffnen
SEND_NOTIFICATION_EMAIL  = True          # True: Sendet eine Benachrichtungsemail für die Terminbuchung 

# ——————————————
# SMTP / E-Mail-Einstellungen (bsp. mit Google SMTP)
# ——————————————
EMPFAENGER       = "Max.Mustermann@abc.de" # Empfänger für eine Benachrichtigungsmail 
ABSENDER         = "Max.SMTPbot@gmail.com" # Absender E-Mail für den Bot
SMTP_SERVER      = "smtp.gmail.com"        # SMTP Server Adresse
SMTP_PORT        = 587                     # SMTP Server Port
SMTP_USER        = ABSENDER                # SMTP Server Benutzer (meist der Absender)
SMTP_PASS        = "xxxx xxxx xxxx xxxx"   # 16-stelliger App-Passwort
