from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class BlankLines(StyleError):

    def __init__(self):
        self._error_code = 'S006'
        super().__init__()

    def check(self, file, lines):
        counter = 0
        line_number = 0
        blank_lines_mistakes = {}

        for line in lines:
            line_number += 1
            if line == '\n':
                counter += 1
            if counter > 2:
                lines_list_rest = lines[line_number:]
                incorrect_line = self._find_first_not_empty_line(lines, lines_list_rest)
                error_message = self.error_messages[self._error_code].format(file, incorrect_line, self._error_code)
                blank_lines_mistakes[error_message] = (PythonFiles.file_name(file), incorrect_line, self._error_code)
                counter = 0
            if line.strip():
                counter = 0
        return blank_lines_mistakes

    @staticmethod
    def _find_first_not_empty_line(whole_list, rest_of_line_list):
        for item in rest_of_line_list:
            if item.strip():
                non_empty = whole_list.index(item) + 1
                return non_empty

