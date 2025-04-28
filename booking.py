"""
booking.py

Führt den vollständigen Buchungsprozess durch:
- Auswahl des Termindatums
- Auswahl des Uhrzeit-Slots
- Ausfüllen des Buchungsformulars
- Bestätigung der Datenschutzbedingung
- (Optional) Abschicken der Buchung
"""
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import config
from utils import retry

# Deutsche Monatsnamen zur Suche
MONTH_NAMES = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]

@retry(times=3, delay=2)
def run_booking_cycle(wsid: str, submit: bool = True, debug: bool = False) -> bool:
    """
    Führt eine Buchungsiteration aus.

    Args:
        wsid: Sitzungsschlüssel
        submit: True zum Absenden, False für Dry-Run
        debug: True, um Browserfenster offen zu halten und vor Schließen zu warten
    """
    url = f"{config.BASE_URL}?uid={config.UID}&wsid={wsid}&lang={config.LANG}"
    options = Options()
    if not debug:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, config.EC_TIMEOUT)

    try:
        logging.info(f"📄 Öffne Terminseite: {url}")
        driver.get(url)

        # --- Schritt 1: Services auswählen ---
        wait.until(EC.presence_of_element_located((By.ID, "step_services")))
        sel = driver.find_elements(By.CSS_SELECTOR, "#step_services select[name$='_amount']")[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sel)
        Select(sel).select_by_index(1)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{ bubbles:true }));", sel)
        wait.until(lambda d: sel.get_attribute("value") == "1")
        driver.find_element(By.CSS_SELECTOR, "button[data-testid='button_next']").click()

        # --- Schritt 2: Gewünschten Monat und Tage auswählen ---
        month_name = MONTH_NAMES[config.TARGET_MONTH - 1]
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".date_cards h4")))
        container = None
        for h in driver.find_elements(By.CSS_SELECTOR, ".date_cards h4"):  # Monat finden
            if month_name in h.text:
                container = h.find_element(By.XPATH, "following-sibling::ol[1]")
                break
        if not container:
            logging.info(f"🔎 Keine Termine im Monat {config.TARGET_MONTH} gefunden – Abbruch.")
            return False

        # Buttons filtern nach Tag und Monat
        date_buttons = container.find_elements(By.CSS_SELECTOR, "button.card.big")
        selected_btn = None
        for btn in date_buttons:
            aria = btn.get_attribute("aria-label")  # z.B. "22.05.2025"
            try:
                day, month, _ = aria.split('.')
                if int(month) == config.TARGET_MONTH and int(day) in config.TARGET_DAYS:
                    selected_btn = btn
                    break
            except:
                continue
        if not selected_btn:
            logging.info(f"🔎 Kein passender Termin für Tage {config.TARGET_DAYS} – Abbruch.")
            return False

        # Datum auswählen
        date_id = selected_btn.get_attribute('id').strip("'")  # z.B. '2025-05-22'
        selected_btn.click()
        logging.info(f"✅ Datum {date_id} gewählt.")

        # --- Schritt 3: Uhrzeit-Slot wählen ---
        # Auf Slot-Container für gewähltes Datum warten
        slot_selector = f".slot_container.day_{date_id} button.card:not(.big)"
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, slot_selector)))
        time_buttons = driver.find_elements(By.CSS_SELECTOR, slot_selector)
        if not time_buttons:
            raise RuntimeError("Keine Uhrzeit-Slots gefunden!")
        # Ersten freien Slot klicken
        time_buttons[0].click()
        logging.info("✅ Uhrzeit ausgewählt.")

        # --- Schritt 4: Buchungsformular ausfüllen ---
        wait.until(EC.url_contains(config.BOOKING_PATH))
        logging.info("📋 Fülle Buchungsformular aus.")
        sal = wait.until(EC.presence_of_element_located((By.NAME, 'salutation')))
        sel_sal = Select(sal)
        try:
            sel_sal.select_by_visible_text(config.SALUTATION)
        except:
            sel_sal.select_by_value(config.SALUTATION)
        for field, value in [('first_name', config.FIRST_NAME), ('last_name', config.LAST_NAME),
                             ('mail', config.EMAIL), ('phone', config.PHONE), ('fin1', config.FIN1)]:
            driver.find_element(By.NAME, field).send_keys(value)
        if config.FIN2:
            driver.find_element(By.NAME, 'fin2').send_keys(config.FIN2)
        if config.FIN3:
            driver.find_element(By.NAME, 'fin3').send_keys(config.FIN3)
        wait.until(EC.element_to_be_clickable((By.NAME, 'accept_data_privacy'))).click()
        logging.info("✅ Formular ausgefüllt.")

        if not submit:
            logging.info("📝 Dry-Run: Buchung nicht abgeschlossen.")
            return True

        # --- Schritt 5: Termin buchen ---
        driver.find_element(By.CSS_SELECTOR, "button[data-testid='button_book-appointment']").click()
        logging.info("🎉 Buchung abgeschlossen.")
        return True

    finally:
        if debug:
            input("Debug-Modus: Drücke Enter zum Schließen...")
        try:
            driver.quit()
        except Exception as e:
            logging.warning(f"⚠️ Fehler beim Schließen: {e}")
