import datetime
import os
from enum import Enum
from decorators import log_execution_time, login_required


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Logger:
    def __init__(
        self,
        print_console: bool = False,
        save_to_log: bool = True,
        user_logined: bool = True,
        log_file_path: str = None,
    ):
        if log_file_path:
            self.log_file = log_file_path
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_file = os.path.join(script_dir, "logs.log")
        self.print_console = print_console
        self.save_to_log = save_to_log
        self.user_logined = user_logined

    @login_required
    @log_execution_time
    def _format_message(self, level: LogLevel, message: str):
        """Format log message"""
        datetime_now = datetime.datetime.now().astimezone().isoformat()
        return f"{datetime_now} - {level.value} - {message}"

    def _save_log(self, message) -> None:
        if self.save_to_log:
            self._save_log_to_file(message)
        if self.print_console:
            print(message)

    def _save_log_to_file(self, message):
        """Save log message in file"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def info(self, message) -> None:
        formatted_message = self._format_message(LogLevel.INFO, message)
        self._save_log(formatted_message)

    def warning(self, message) -> None:
        formatted_message = self._format_message(LogLevel.WARNING, message)
        self._save_log(formatted_message)

    def error(self, message) -> None:
        formatted_message = self._format_message(LogLevel.ERROR, message)
        self._save_log(formatted_message)
