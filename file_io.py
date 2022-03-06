import csv
import os.path


class NotSQlFileError(Exception):
    pass


class SQLFileReader:

    def __init__(self, file_path: str):
        path, extension = os.path.splitext(file_path)
        if extension != '.sql':
            raise NotSQlFileError()
        self.path = path + extension

    # Reads from the file and expects the delimiters to be a ';'
    def read_statements(self) -> list[str]:
        all_lines = self.__read_all_lines()
        statements = all_lines.split(';')[:-1]
        return statements

    def __read_all_lines(self) -> str:
        all_lines = ''
        with open(self.path, 'r') as file:
            for line in file:
                all_lines += line.strip()
        return all_lines