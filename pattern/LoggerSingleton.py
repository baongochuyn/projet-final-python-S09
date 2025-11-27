from threading import Lock
from datetime import datetime

class LoggerSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._log_file = "logs/marketing.log"
        return cls._instance

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        with open(self._log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")


