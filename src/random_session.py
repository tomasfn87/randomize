from datetime import datetime as dt
from os import path
from src.random import Random
from tools.color import print_color
from tools.file_tools import FileTools
from tools.string_tools import StringTools

class RandomSession:
    def __init__(
        self, list_to_randomize, last_result, already_randomized, no_repeat):
        self.list_to_randomize  = list_to_randomize
        self.last_result        = last_result
        self.already_randomized = already_randomized
        self.no_repeat          = no_repeat

    def session(self):
        FileTools.create_template_file(self.last_result, {})
        FileTools.create_template_file(self.list_to_randomize, {
            "result_description": "my next trip will be to",
            "options": ["Portugal", "Spain", "France", "Italy"]})

        last_result_data = FileTools.read_json_file(
            self.last_result, default_content={})
        list_to_randomize_data = FileTools.read_json_file(
            self.list_to_randomize, default_content={
                "result_description": "my next trip will be to",
                "options": ["Portugal", "Spain", "France", "Italy"]})

        result_description = list_to_randomize_data.get(
            "result_description", "")

        options = list_to_randomize_data.get("options", [])

        if len(StringTools.deduplicate(options)) < len(options):
            print_color("ERROR", "red", end="")
            print(": duplicated options were detected.")
            FileTools.fix_file(self.list_to_randomize)
            return

        if len(options) < 2:
            print_color("ERROR", "red", end="")
            if len(options) == 1:
                print(": the only option is:", end=" ")
                print_color(options[0].strip(), "light yellow", end="")
                print(".")
            else:
                print(": no options were defined.")
            FileTools.fix_file(self.list_to_randomize)
            return

        if not result_description.strip():
            print_color("ERROR", "red", end="")
            print(": invalid result description.")
            FileTools.fix_file(self.list_to_randomize)
            return

        already_randomized_data = ""
        all_options_randomized_count = 0
        if self.no_repeat:
            already_randomized_path = self.already_randomized

            if path.exists(already_randomized_path):
                already_randomized_data = FileTools.read_json_file(
                    already_randomized_path, default_content={
                        "all_options_randomized_count": 0,
                        "already_randomized": []})
            else:
                FileTools.create_template_file(already_randomized_path, {
                    "all_options_randomized_count": 0,
                    "already_randomized": []})
                already_randomized_data = {
                    "all_options_randomized_count": 0,
                    "already_randomized": []}

            all_options_randomized_count = already_randomized_data.get(
                "all_options_randomized_count", 0)
            already_randomized = already_randomized_data.get(
                "already_randomized", [])

            if len(already_randomized) < all_options_randomized_count + 1:
                already_randomized_data["already_randomized"].insert(0, {
                    "datetime": str(dt.now())[0:19],
                    "comments": [], "selected": []})

            results = already_randomized[0]["selected"]

            actual_options = []
            if already_randomized and results:
                actual_options = results

            if len(actual_options) >= len(options):
                actual_options = []

        total_options = len(options)
        if self.no_repeat and actual_options:
            options = [name for name in options if name not in actual_options]

        last_result = last_result_data.get("last_result")

        position = 0
        if self.no_repeat:
            position = len(results) + 1

        r = Random(result_description, options, last_result)
        new_result = r.randomizer(
            total_options  = total_options,
            position       = position,
            no_repeat      = self.no_repeat,
            cycle_count    = all_options_randomized_count)

        if new_result is not None:
            last_result_data["last_result"] = new_result
            FileTools.write_json_file(self.last_result, last_result_data)

        if self.no_repeat:
            results.append(new_result)

            if len(results) >= total_options:
                already_randomized_data["all_options_randomized_count"] += 1
                all_options_randomized_count += 1

            print_color("Times list was completed:", "dim", end=" ")
            if all_options_randomized_count == 0:
                print_color(all_options_randomized_count, "red")
            else:
                if all_options_randomized_count % 2 == 0:
                    print_color(all_options_randomized_count, "light yellow")
                else:
                    print_color(all_options_randomized_count, "light green")

            FileTools.write_json_file(
                already_randomized_path, already_randomized_data)
