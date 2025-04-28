"""
utils.py

Enthält Hilfsfunktionen für den Terminbot:
- sleep_random: Wartet zufällig zwischen zwei Intervallen.
- retry: Decorator für mehrfaches Wiederholen bei Fehlern.
"""

import time
import random
import logging
from functools import wraps

def sleep_random(min_seconds: float, max_seconds: float) -> None:
    """Schläft eine zufällige Dauer zwischen min_seconds und max_seconds."""
    duration = random.uniform(min_seconds, max_seconds)
    logging.info(f"⏱️ Pausiere für {duration:.1f} Sekunden")
    time.sleep(duration)

def retry(times: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorator, der eine Funktion bei Auftreten bestimmter Exceptions mehrfach ausführt.

    :param times: Anzahl der Versuche
    :param delay: Pause zwischen den Versuchen in Sekunden
    :param exceptions: Tuple der Exception-Typen, bei denen erneut versucht wird
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
