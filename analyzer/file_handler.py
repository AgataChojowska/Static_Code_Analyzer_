import os


class PythonFiles:

    @staticmethod
    def get_python_files(fpath):
        paths_to_check = []
        if os.path.isfile(fpath) and fpath.endswith('.py'):
            paths_to_check.append(fpath)
        if os.path.isdir(fpath):
            for file in os.listdir(fpath):
                if file.endswith(".py"):
                    paths_to_check.append(os.path.join(fpath, file))
        return paths_to_check

    @staticmethod
    def file_name(path_):
        return path_.split('/')[-1]