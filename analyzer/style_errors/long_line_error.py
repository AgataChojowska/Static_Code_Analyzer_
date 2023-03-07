from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class LongLine(StyleError):

    def __init__(self):
        self._max_chars = 79
        self._error_code = 'S001'
        super().__init__()

    @property
    def max_chars(self):
        return self._max_chars

    @max_chars.setter
    def max_chars(self, new_max_chars):
        if isinstance(new_max_chars, int):
            self._max_chars = new_max_chars
        else:
            raise ValueError("Max chars has to be an int.")

    def check(self, file, lines):
        line_number = 0
        length_mistakes = {}
        for line in lines:
            line_number += 1
            if len(line) > self._max_chars:
                error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                length_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return length_mistakes