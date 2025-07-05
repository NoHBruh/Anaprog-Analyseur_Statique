from enum import Enum

class WarningType(Enum):
    WARNING = "[WARNING]"
    ERROR = "[ERROR]"

class Warnings:
    def __init__(self):
        self.warnings = []

    def add_warning(self, type: WarningType, message):
        self.warnings.append((type, message))

    def print_warnings(self):
        for warning in self.warnings:
            print(warning[0].value + " - " + warning[1])