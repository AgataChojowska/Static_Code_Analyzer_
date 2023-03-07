import pathlib

import pytest
import ast
from analyzer.style_errors.long_line_error import LongLine
from analyzer.style_errors.to_do_error import ToDo
from analyzer.style_errors.indent_error import Indent
from analyzer.style_errors.semicolon_error import Semicolon
from analyzer.style_errors.inline_comment_error import InlineComment
from analyzer.style_errors.blank_lines_error import BlankLines
from analyzer.style_errors.construction_name_error import ConstructionName
from analyzer.style_errors.class_name_error import ClassName
from analyzer.style_errors.function_name_error import FunctionName
from analyzer.style_errors.argument_name_error import ArgumentName
from analyzer.style_errors.variable_name_error import VariableName
from analyzer.style_errors.mutable_default_argument_error import DefaultArgument


class TestLongLine:

    def test_max_chars(self):
        ll = LongLine()
        assert ll.max_chars == 79
        ll.max_chars = 80
        assert ll.max_chars == 80
        with pytest.raises(ValueError):
            ll.max_chars = "not an int"

    def test_check_one_error(self):
        ll = LongLine()
        lines = ["this is a short line",
                 "This is a veeeeeeeeeeeeeeeeeeeeeeeeeeeeeery loooooooooooooooooooooooooong liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiine"]
        result = ll.check("Users/path/some_file.py", lines)
        expected_error = "Users/path/some_file.py: Line 2: S001 Too long"
        assert result[expected_error] == ('some_file.py', 2, "S001")

    def test_multiple_errors(self):
        ll = LongLine()
        lines = [
            "This is a veeeeeeeeeeeeeeeeeeeeeeeeeeeeeery loooooooooooooooooooooooooong liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiine",
            "This is a veeeeeeeeeeeeeeeeeeeeeeeeeeeeeery loooooooooooooooooooooooooong liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiine"]
        result = ll.check("Users/path/some_file.py", lines)
        error_message = 'Users/path/some_file.py: Line 1: S001 Too long'
        error_message_2 = 'Users/path/some_file.py: Line 2: S001 Too long'
        assert result == {f'{error_message}': ('some_file.py', 1, 'S001'),
                          f'{error_message_2}': ('some_file.py', 2, 'S001')}

    def test_check_no_errors(self):
        ll = LongLine()
        lines = ["short line", "also a short line", "goddammit this line is short"]
        result = ll.check("Users/path/some_file.py", lines)
        assert not result


class TestIndent:

    def test_check_one_error(self):
        ii = Indent()
        lines = ["Lack of intent", "    Correct indent", "   Incorrect indent"]
        result = ii.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S002 Indentation is not a multiple of four"
        assert result[error_message] == ('some_file.py', 3, 'S002')

    def test_check_multiple_errors(self):
        ii = Indent()
        lines = ["Lack of intent", "    Correct indent", "   Incorrect indent", "  Also incorrect indent"]
        result = ii.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S002 Indentation is not a multiple of four"
        error_message_2 = "Users/path/some_file.py: Line 4: S002 Indentation is not a multiple of four"
        assert result == {
            f"{error_message}": ('some_file.py', 3, 'S002'),
            f"{error_message_2}": ('some_file.py', 4, 'S002')
        }

    def test_check_no_errors(self):
        ii = Indent()
        lines = ["Lack of intent", "    Correct indent", "        Also correct"]
        result = ii.check("Users/path/some_file.py", lines)
        assert not result


class TestSemicolon:

    def test_check_one_error(self):
        ss = Semicolon()
        lines = ["Correct line", "Trailing semicolon;;;", "Trailing semicolon in a comment  # which is correct;;"]
        result = ss.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 2: S003 Unnecessary semicolon after a statement"
        assert result[error_message] == ('some_file.py', 2, 'S003')

    def test_check_multiple_errors(self):
        ss = Semicolon()
        lines = ["Incorrect line;", "Trailing semicolon;;;", "# Trailing semicolon in a comment which is correct;;"]
        result = ss.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 1: S003 Unnecessary semicolon after a statement"
        error_message_2 = "Users/path/some_file.py: Line 2: S003 Unnecessary semicolon after a statement"
        assert result == {
            f"{error_message}": ('some_file.py', 1, 'S003'),
            f"{error_message_2}": ('some_file.py', 2, 'S003')
        }

    def test_check_no_errors(self):
        ss = Semicolon()
        lines = ["Correct line", "Semicolon # in inline comment;", "# Trailing semicolon in a comment;;"]
        result = ss.check("Users/path/some_file.py", lines)
        assert not result


class TestInlineComment:

    def test_check_one_error(self):
        ic = InlineComment()
        lines = ["incorrect # inline comment", "correct  # 2 spaces before inline comment"]
        result = ic.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 1: S004 Less than two spaces before inline comments"
        assert result[error_message] == ('some_file.py', 1, 'S004')

    def test_check_multiple_errors(self):
        ic = InlineComment()
        lines = ["incorrect # inline comment", "correct  # 2 spaces before inline comment", "incorrect# comment"]
        result = ic.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 1: S004 Less than two spaces before inline comments"
        error_message_2 = "Users/path/some_file.py: Line 3: S004 Less than two spaces before inline comments"
        assert result == {
            f"{error_message}": ('some_file.py', 1, 'S004'),
            f"{error_message_2}": ('some_file.py', 3, 'S004')
        }

    def test_check_no_errors(self):
        ic = InlineComment()
        lines = ["correct  # inline comment", "correct  # 2 spaces before inline comment"]
        result = ic.check("Users/path/some_file.py", lines)
        assert not result


class TestToDo:

    def test_check_one_error(self):
        ttd = ToDo()
        lines = ["correct, TODO but not in comment", "# todo in a comment"]
        result = ttd.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 2: S005 TODO found"
        assert result[error_message] == ('some_file.py', 2, 'S005')

    def test_check_multiple_errors(self):
        ttd = ToDo()
        lines = ["correct, TODO but not in comment", "# todo in a comment", "text  # TODO in inline comment"]
        result = ttd.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 2: S005 TODO found"
        error_message_2 = "Users/path/some_file.py: Line 3: S005 TODO found"
        assert result == {
            f"{error_message}": ('some_file.py', 2, 'S005'),
            f"{error_message_2}": ('some_file.py', 3, 'S005')
        }

    def test_check_no_errors(self):
        ttd = ToDo()
        lines = ["correct", "todo but not in a comment so correct", "TODO but not in comment"]
        result = ttd.check("Users/path/some_file.py", lines)
        assert not result


class TestBlankLines:

    def test_check_two_errors(self):
        bl = BlankLines()
        lines = ['\n', '\n', '\n', 'text', '\n', '\n', 'more text', '\n', '\n', '\n', '\n', 'some more text']
        result = bl.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 4: S006 More than two blank lines preceding a code line"
        error_message_2 = "Users/path/some_file.py: Line 12: S006 More than two blank lines preceding a code line"
        assert result == {
            f"{error_message}": ('some_file.py', 4, 'S006'),
            f"{error_message_2}": ('some_file.py', 12, 'S006')
        }

    def test_check_no_errors(self):
        bl = BlankLines()
        lines = ['\n', '\n', 'text', '\n', '\n', 'more text', '\n', 'some more text']
        result = bl.check("Users/path/some_file.py", lines)
        assert not result


class TestConstructionName:

    def test_check_one_error(self):
        cn = ConstructionName()
        lines = ['def correct', 'class CorrectClass', 'def    incorrect_class']
        result = cn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S007 Too many spaces after construction_name"
        assert result[error_message] == ('some_file.py', 3, 'S007')

    def test_check_multiple_errors(self):
        cn = ConstructionName()
        lines = ['def correct', 'class CorrectClass', 'def    incorrect_class', 'class  IncorrectClass', 'not a class']
        result = cn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S007 Too many spaces after construction_name"
        error_message_2 = "Users/path/some_file.py: Line 4: S007 Too many spaces after construction_name"
        assert result == {f"{error_message}": ("some_file.py", 3, "S007"),
                          f"{error_message_2}": ("some_file.py", 4, "S007")}

    def test_check_no_errors(self):
        cn = ConstructionName()
        lines = ['def correct', 'class Correct', 'text']
        result = cn.check("Users/path/some_file.py", lines)
        assert not result


class TestClassName:

    def test_check_one_error(self):
        cn = ClassName()
        lines = ['class Correct', 'class AlsoCorrect', 'class not_correct']
        result = cn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S008 Class name should be written in CamelCase"
        assert result[error_message] == ("some_file.py", 3, "S008")

    def test_check_multiple_errors(self):
        cn = ClassName()
        lines = ['class Correct', 'class AlsoCorrect', 'class not_correct', 'class noTCorrect']
        result = cn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S008 Class name should be written in CamelCase"
        error_message_2 = "Users/path/some_file.py: Line 4: S008 Class name should be written in CamelCase"
        assert result == {error_message: ("some_file.py", 3, "S008"),
                          error_message_2: ("some_file.py", 4, "S008")}

    def test_check_no_errors(self):
        cn = ClassName()
        lines = ['class Correct', 'class AlsoCorrect']
        result = cn.check("Users/path/some_file.py", lines)
        assert not result


class TestFunctionName:

    def test_check_one_error(self):
        fn = FunctionName()
        lines = ['def correct_function', 'not a function', 'def IncorrectFunction']
        result = fn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S009 Function name should be written in snake_case"
        assert result[error_message] == ("some_file.py", 3, "S009")

    def test_check_multiple_errors(self):
        fn = FunctionName()
        lines = ['def correct_function', 'not a function', 'def IncorrectFunction', 'def incorrectFunction',
                 'def Incor']
        result = fn.check("Users/path/some_file.py", lines)
        error_message = "Users/path/some_file.py: Line 3: S009 Function name should be written in snake_case"
        error_message_2 = "Users/path/some_file.py: Line 4: S009 Function name should be written in snake_case"
        error_message_3 = "Users/path/some_file.py: Line 5: S009 Function name should be written in snake_case"
        assert result == {f"{error_message}": ("some_file.py", 3, "S009"),
                          f"{error_message_2}": ("some_file.py", 4, "S009"),
                          f"{error_message_3}": ("some_file.py", 5, "S009")}

    def test_check_no_errors(self):
        fn = FunctionName()
        lines = ['def correct_function', 'not a function', 'def correct']
        result = fn.check("Users/path/some_file.py", lines)
        assert not result


class TestArgumentName:

    def test_check_one_error(self):
        an = ArgumentName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_10/class_10_one_error.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = an.check(_path, tree)
        error_message = f"{_path}: Line 1: S010 Argument name 'NAME' should be written in snake_case"
        assert result[error_message] == ('class_10_one_error.py', 1, "S010")

    def test_check_multiple_errors(self):
        an = ArgumentName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_10/class_10_multiple_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = an.check(_path, tree)
        error_message = f"{_path}: Line 1: S010 Argument name 'NAME' should be written in snake_case"
        error_message_2 = f"{_path}: Line 5: S010 Argument name 'Name' should be written in snake_case"
        error_message_3 = f"{_path}: Line 9: S010 Argument name 'Name' should be written in snake_case"
        error_message_4 = f"{_path}: Line 9: S010 Argument name 'AGE' should be written in snake_case"
        assert result == {f"{error_message}": ('class_10_multiple_errors.py', 1, "S010"),
                          f"{error_message_2}": ('class_10_multiple_errors.py', 5, "S010"),
                          f"{error_message_3}": ('class_10_multiple_errors.py', 9, "S010"),
                          f"{error_message_4}": ('class_10_multiple_errors.py', 9, "S010")}

    def test_check_no_errors(self):
        an = ArgumentName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_10/class_10_no_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = an.check(_path, tree)
        assert not result


class TestVariableName:

    def test_check_one_error(self):
        vn = VariableName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_11/class_11_one_error.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = vn.check(_path, tree)
        error_message = f"{_path}: Line 2: S011 Variable 'VARIABLE' should be written in snake_case"
        assert result[error_message] == ('class_11_one_error.py', 2, "S011")

    def test_check_multiple_errors(self):
        vn = VariableName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_11/class_11_multiple_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = vn.check(_path, tree)
        error_message = f"{_path}: Line 2: S011 Variable 'VARIABLE' should be written in snake_case"
        error_message_2 = f"{_path}: Line 3: S011 Variable 'AnotherVariable' should be written in snake_case"
        assert result == {f"{error_message}": ('class_11_multiple_errors.py', 2, "S011"),
                          f"{error_message_2}": ('class_11_multiple_errors.py', 3, "S011")
                          }

    def test_check_no_errors(self):
        vn = VariableName()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_11/class_11_no_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = vn.check(_path, tree)
        assert not result


class TestDefaultArgument:

    def test_check_one_error(self):
        da = DefaultArgument()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_12/class_12_one_error.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = da.check(_path, tree)
        error_message = f"{_path}: Line 1: S012 The default argument value is mutable"
        assert result[error_message] == ('class_12_one_error.py', 1, "S012")

    def test_check_multiple_errors(self):
        da = DefaultArgument()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_12/class_12_multiple_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = da.check(_path, tree)
        error_message = f"{_path}: Line 1: S012 The default argument value is mutable"
        error_message_2 = f"{_path}: Line 5: S012 The default argument value is mutable"
        assert result == {f"{error_message}": ('class_12_multiple_errors.py', 1, "S012"),
                          f"{error_message_2}": ('class_12_multiple_errors.py', 5, "S012")
                          }

    def test_check_no_errors(self):
        da = DefaultArgument()
        _path = f"{pathlib.Path(__file__).parent}/Test_Files/class_12/class_12_no_errors.py"
        with open(_path, 'r', encoding='UTF-8') as file:
            tree = ast.parse(file.read())
        result = da.check(_path, tree)
        assert not result
