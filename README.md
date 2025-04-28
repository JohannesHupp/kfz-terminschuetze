# **KFZ Terminschütze**

**Ein automatisierter Bot zur Buchung von Fahrzeugzulassungsterminen für die Stadt Köln.**

## **Inhaltsverzeichnis**

- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
- [Architektur](#architektur)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Debugging & Dry-Run](#debugging--dry-run)
- [Logging](#logging)
- [Benachrichtigungen](#benachrichtigungen)
- [Beitragende](#beitragende)
- [Lizenz](#lizenz)

---

## Über das Projekt

Der **KFZ Termin Bot** automatisiert den Prozess der Terminbuchung auf der Website der Stadt Köln für Kfz-Zulassungstermine. Er prüft in regelmäßigen Abständen verfügbare Termine im konfigurierten Monat und an den gewünschten Tagen. Bei erfolgreicher Buchung wird eine Benachrichtigungs-E-Mail verschickt, danach beendet sich das Programm.

## Funktionen

- Automatisierte Anmeldung und Sitzungs-ID-Abruf (`wsid_fetcher.py`)
- Auswahl von Service, Datum und Uhrzeit mittels Selenium (`booking.py`)
- Konfigurierbare Zieltermine (Monat & Tage) und Buchungsdaten (`config.py`)
- Zufällige Warteintervalle zwischen den Prüfzyklen (`utils.py`)
- Wiederholungs-Mechanismen bei Fehlern (Retry-Decorator)
- E-Mail-Benachrichtigung bei erfolgreicher Buchung (konfigurierbar via `SEND_NOTIFICATION_EMAIL`, `notifier.py`)
- Headless- und Debug-Modus
- Ausführliches Logging in Datei und Konsole

## Architektur

```
main.py      # Koordination: WSID holen, Buchungs-Loop, Notifikation
 ├── wsid_fetcher.py  # Holt WSID via Redirect-Header
 ├── booking.py       # Füllt Terminformular aus und bucht
 ├── notifier.py      # Sendet E-Mail-Benachrichtigung
 └── utils.py         # Helfer: sleep_random, retry-Decorator
 config.py    # Alle Einstellungen (URLs, Zieltermine, Credentials)
 terminbot.log # Logdatei
```

## Voraussetzungen

- Python 3.8+
- Google Chrome oder Chromium
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (passend zur Chrome-Version)
- Internetzugang zum Terminportal

## Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/JohannesHupp/kfz-terminschuetze.git
   cd kfz-terminschuetze
   ```
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. ChromeDriver ins Systempath legen oder Pfad anpassen.

## Konfiguration

Alle Einstellungen befinden sich in der Datei `config.py`:

- **TECHNISCHE PARAMETER**

  - `BASE_URL`: Basis-URL des Terminportals
  - `UID`: Deine eindeutige User-ID
  - `LANG`: UI-Sprache (z.B. "de")
  - `EC_TIMEOUT`: Timeout für Selenium-ExpectedConditions
  - `BOOKING_PATH`: Teil der URL für die Buchungsseite

- **ZIELTERMINE**

  - `TARGET_MONTH`: Zielmonat (Nummer, z.B. 4 = April)
  - `TARGET_DAYS`: Liste gewünschter Tage im Monat (z.B. `[21, 22, 23]`)

- **WARTEINTERVALLE**

  - `MIN_WAIT_SECONDS`, `MAX_WAIT_SECONDS`: Pause zwischen Prüfzyklen

- **PERSÖNLICHE DATEN**

  - `SALUTATION`, `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `PHONE`, `FIN1`, `FIN2`, `FIN3`

- **ABLAUFSTEUERUNG**

  - `SUBMIT`: Bei `False` erfolgt nur ein Dry-Run.  - `DEBUG`: Bei `True` bleibt das Browserfenster offen.
  - `SEND_NOTIFICATION_EMAIL`: Bei `True` wird nach erfolgreicher Buchung eine E-Mail verschickt; bei `False` erfolgt keine Benachrichtigung.

- **SMTP / E-MAIL**

  - `ABSENDER`, `EMPFAENGER`, `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`

Passe diese Werte an deine Gegebenheiten an.

## Verwendung

Nach Installation und Konfiguration kannst du den Bot starten:

```bash
python main.py
```

Der Bot läuft in einer Endlosschleife:

1. Holt die WSID
2. Prüft verfügbare Termine
3. Bucht den ersten passenden Termin
4. Sendet E-Mail bei Erfolg und beendet sich
5. Bei keinem Treffer: Pause & nächster Versuch

## Debugging & Dry-Run

- **Dry-Run**: Setze `SUBMIT = False` in `config.py`, um das Buchen zu simulieren.
- **Debug-Modus**: Setze `DEBUG = True`, um das Browserfenster sichtbar zu lassen. Nützlich zum Entwickeln oder Testen.

## Logging

Logs werden in `terminbot.log` und in der Konsole ausgegeben. Das Log enthält:

- Info- und Fehlermeldungen
- Anzahl und Dauer der Versuche
- Ausgewähltes Datum und Zeit

## Benachrichtigungen

Nach erfolgreicher Terminbuchung verschickt der Bot eine E-Mail. Die Funktionalität ist implementiert in `notifier.py`. Stelle sicher, dass deine SMTP-Daten korrekt sind.

## Beitragende

- **Autor**: Johannes Hupp
- **Lizenz**: Siehe unten

## Lizenz

Dieses Projekt steht unter der [MIT Lizenz](LICENSE).

## Rechtlicher Zusatz-Hinweis (Disclaimer)

Dieses Softwareprojekt interagiert automatisiert mit externen Websites (z.B. Terminportalen). Bitte beachte, dass die Nutzung dieser Software auf eigene Verantwortung erfolgt. 

Es wird ausdrücklich darauf hingewiesen, dass durch die Verwendung dieser Software möglicherweise gegen die Nutzungsbedingungen der jeweiligen Anbieter verstoßen werden kann. Der Autor übernimmt keinerlei Haftung für eventuelle Sperrungen, rechtliche Konsequenzen oder Schäden, die aus der Verwendung dieser Software resultieren.

Die Software ist ausschließlich für private, nicht-kommerzielle Zwecke sowie zu Test- und Lernzwecken bestimmt.

Nutzer sind angehalten, die jeweils gültigen Nutzungsbedingungen und gesetzlichen Vorgaben eigenständig zu prüfen und einzuhalten.

