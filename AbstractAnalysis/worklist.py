from abstract_flow import AbstractEnvironment
from abstractDomain import AbstractDomain
from .warnings import Warnings, WarningType
class Worklist:
    def __init__(self):
        self.array_sizes = {} # used for keeping tracks of array sizes, facilitates checking when using a constant as index
        self.abstract_environement = AbstractEnvironment()
        self.conditions = []
        self.warnings = Warnings()
        self.work_list = []