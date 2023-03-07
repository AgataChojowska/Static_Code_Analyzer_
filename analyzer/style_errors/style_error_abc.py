from abc import ABC, abstractmethod


class StyleError(ABC):

    def __init__(self):
        self.error_messages = {
            "S001": "{}: Line {}: {} Too long",
            "S002": "{}: Line {}: {} Indentation is not a multiple of four",
            "S003": "{}: Line {}: {} Unnecessary semicolon after a statement",
            "S004": "{}: Line {}: {} Less than two spaces before inline comments",
            "S005": "{}: Line {}: {} TODO found",
            "S006": "{}: Line {}: {} More than two blank lines preceding a code line",
            "S007": "{}: Line {}: {} Too many spaces after construction_name",
            "S008": "{}: Line {}: {} Class name should be written in CamelCase",
            "S009": "{}: Line {}: {} Function name should be written in snake_case",
            "S010": "{}: Line {}: {} Argument name '{}' should be written in snake_case",
            "S011": "{}: Line {}: {} Variable '{}' should be written in snake_case",
            "S012": "{}: Line {}: {} The default argument value is mutable"
        }

    @abstractmethod
    def check(self, file, structure):
        pass
