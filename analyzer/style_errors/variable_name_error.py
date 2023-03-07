import re
import ast
from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class VariableName(StyleError):

    def __init__(self):
        self._error_code = 'S011'
        super().__init__()

    def check(self, file, tree):
        blank_lines_mistakes = {}
        variable_names = []
        incorrect_name = r'_?_?[A-Z]+'
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                variable_name = node.id
                if variable_name in variable_names:
                    break
                variable_names.append(variable_name)
                if re.match(incorrect_name, variable_name):
                    line_number = node.lineno
                    error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code,
                                                                                 variable_name)
                    blank_lines_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return blank_lines_mistakes

