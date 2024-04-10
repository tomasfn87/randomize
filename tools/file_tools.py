from json import dump, load
from tools.color import print_color
from os import stat
from os.path import exists

class FileTools:
    @staticmethod
    def read_json_file(file_path, default_content=None):
        if not exists(file_path) or stat(file_path).st_size == 0:
            return default_content
        with open(file_path, "r", encoding="utf-8") as file:
            data = load(file)
        return data

    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, "w") as file:
            dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def create_template_file(file_path, template_content):
        if not exists(file_path) or stat(file_path).st_size == 0:
            FileTools.write_json_file(file_path, template_content)

    @staticmethod
    def fix_file(file_name):
        print("Please edit file", end=" ")
        print_color(file_name.strip(), "yellow", end=" ")
        print("before continuing.")
