"""
utils.py

Stellt Hilfsfunktionen für den KFZ Terminbot bereit.

Funktionen:
- sleep_random: Pausiert für eine zufällige Dauer zwischen zwei Intervallen.
- retry: Dekorator zur Wiederholung von Funktionsaufrufen bei Fehlern.

Wird genutzt in:
- main.py, wsid_fetcher.py und booking.py
"""

import time
import random
import logging
from functools import wraps

def sleep_random(min_seconds: float, max_seconds: float) -> None:
    """
    Pausiert für eine zufällige Dauer zwischen min_seconds und max_seconds.

    Args:
        min_seconds (float): Minimale Pausenzeit in Sekunden.
        max_seconds (float): Maximale Pausenzeit in Sekunden.
    """
    duration = random.uniform(min_seconds, max_seconds)
    logging.info(f"⏱️ Pausiere für {duration:.1f} Sekunden")
    time.sleep(duration)

def retry(times: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Dekorator, der eine Funktion bei bestimmten Fehlern mehrfach erneut ausführt.

    Args:
        times (int): Maximale Anzahl der Versuche.
        delay (float): Wartezeit in Sekunden zwischen den Versuchen.
        exceptions (tuple): Exception-Typen, bei denen ein neuer Versuch gestartet wird.

    Returns:
        Callable: Die dekorierte Funktion mit Wiederhol-Logik.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    logging.warning(
                        f"⚠️ Versuch {attempt}/{times} für {func.__name__} fehlgeschlagen: {e}"
                    )
                    if attempt < times:
                        time.sleep(delay)
                    else:
                        logging.error(
                            f"❌ Alle {times} Versuche für {func.__name__} fehlgeschlagen."
                        )
                        raise
        return wrapper
    return decorator
