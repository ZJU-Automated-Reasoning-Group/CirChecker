from enum import Enum
import colorama
from AST import FileLocation

colorama.init(autoreset=True)


class ReportType(Enum):
    ERROR = "Error"
    WARNING = "Warning"


class Report(Exception):
    def __init__(self, type_: ReportType, location: FileLocation, message: str, has_location: bool = True):
        self.type = type_
        self.location = location
        self.message = message
        self.has_location = has_location

    def __str__(self):
        color = colorama.Fore.RED if self.type == ReportType.ERROR else colorama.Fore.YELLOW
        prefix = f"{color}[{self.type.value}]{colorama.Style.RESET_ALL}"
        path = self.location.path
        if self.has_location:
            line = self.location.start.line
            col = self.location.start.column
            location_str = f"{path}:{line}:{col}"
        else:
            location_str = path
        return f"{prefix}    In {location_str}\n{' ' * 13}{self.message}"

    def show(self):
        print(self.__str__())
