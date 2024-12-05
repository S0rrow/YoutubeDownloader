import os
from datetime import datetime, timezone, timedelta
from threading import Lock

# Constants for log levels
LOG_LEVELS = {
    0: "DEBUG",
    1: "ERROR",
    2: "WARN",
    3: "STATUS",
    4: "INFO"
}

class Logger:
    """
    A logger class for generating log messages.
    - path: Directory where log files will be stored.
    - options: Dictionary for logger configuration.
        - name(optional): Name of the source logger (defaults to __name__ of the calling module).
    """
    def __init__(self, options: dict = None, path: str = None):
        parent_path = os.path.dirname(os.path.abspath(__file__))
        self.path = path or os.path.join(parent_path, "logs")
        self.options = options or {}
        self.lock = Lock()

        # Ensure the log directory exists
        os.makedirs(self.path, exist_ok=True)

    def log(self, msg: str, flag: int = 0, name: str = None):
        """
        Save log messages based on log level.
        - msg: Log message.
        - flag: Log level (0: DEBUG, 1: ERROR, 2: WARN, 3: STATUS, 4: INFO).
        - name: Name of the logger (defaults to options['name'] or the calling module's __name__).
        """
        if flag not in LOG_LEVELS:
            raise ValueError(f"Invalid log level: {flag}. Valid levels are: {list(LOG_LEVELS.keys())}")

        # Get logger name
        name = name or self.options.get("name", __name__)

        # Get current timestamp in KST (UTC+9)
        utc_now = datetime.now(timezone.utc)
        kst_now = utc_now + timedelta(hours=9)
        now = kst_now.strftime("%Y-%m-%d %H:%M:%S")

        # Format log message
        log_type = LOG_LEVELS[flag]
        log_message = f"[{now}][{log_type}]({name}) > {msg.replace(os.linesep, ' ')}\n"

        # Write to log file
        log_file = os.path.join(self.path, f"{log_type}.log")
        with self.lock:  # Ensure thread safety
            with open(log_file, "a") as f:
                f.write(log_message)
