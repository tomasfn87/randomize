from datetime import datetime as dt
from tools.color import print_color
from tools.file_tools import FileTools
from tools.string_tools import StringTools
import os
import random
import sys

class Random:
    def __init__(self, result_description, options, last_result):
        self.result_description = result_description or ""
        self.options = options or []
        self.last_result = last_result or ""

    def randomizer(self, total_options, position, no_repeat, cycle_count):

        description = self.result_description.capitalize()

        options = [name for name in self.options if name != self.last_result]
        if options:
            random_result = random.choice(options)
            print(f"{description}:\n- ",  end="")
            if no_repeat and position == total_options:
                if cycle_count % 2 == 0:
                    print_color(random_result.strip(), "light green", end="")
                else:
                    print_color(random_result.strip(), "light yellow", end="")
            elif cycle_count % 2 == 0:
                print_color(
                    random_result.strip(), "light cyan", end="")
            else:
                print_color(
                    random_result.strip(), "light blue", end="")
            if no_repeat:
                print(" (", end="")
                if position == total_options:
                    if cycle_count % 2 == 0:
                        print_color(position, "light green", end="")
                    else:
                        print_color(position, "light yellow", end="")
                else:
                    print_color(position, "dim", end="")
                print("/", end="")
                if position == total_options:
                    if cycle_count % 2 == 0:
                        print_color(total_options, "light green", end="")
                    else:
                        print_color(total_options, "light yellow", end="")
                else:
                    print(total_options, end="")
                print(")", end="")
            print()
            if random_result is not None:
                return random_result
        else:
            print("All options were selected. Let's start next round!")
            return None

def main():
    no_repeat = False
    if "--no-repeat" in [arg.lower() for arg in sys.argv]:
        no_repeat = True

    last_result_data = FileTools.read_json_file(
        "lastResult.json", default_content={})
    list_to_randomize_data = FileTools.read_json_file(
        "listToRandomize.json", default_content={
            "result_description": "my next trip will be to",
            "options": ["Portugal", "Spain", "France", "Italy"]})

    result_description = list_to_randomize_data.get(
        "result_description", "")

    options = list_to_randomize_data.get("options", [])

    if len(StringTools.deduplicate(options)) < len(options):
        print_color("ERROR", "red", end="")
        print(": duplicated options were detected.")
        FileTools.fix_file("listToRandomize.json")
        return

    if len(options) < 2:
        print_color("ERROR", "red", end="")
        if len(options) == 1:
            print(": the only option is:", end=" ")
            print_color(options[0].strip(), "light yellow", end="")
            print(".")
        else:
            print(": no options were defined.")
        FileTools.fix_file("listToRandomize.json")
        return

    if not result_description.strip():
        print_color("ERROR", "red", end="")
        print(": invalid result description.")
        FileTools.fix_file("listToRandomize.json")
        return

    already_randomized_data = ""
    all_options_randomized_count = 0
    if no_repeat:
        already_randomized_path = "alreadyRandomized.json"

        if os.path.exists(already_randomized_path):
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
    if no_repeat and actual_options:
        options = [name for name in options if name not in actual_options]

    last_result = last_result_data.get("last_result")

    position = 0
    if no_repeat:
        position = len(results) + 1

    r = Random(result_description, options, last_result)
    new_result = r.randomizer(
        total_options  = total_options,
        position       = position,
        no_repeat      = no_repeat,
        cycle_count    = all_options_randomized_count)

    if new_result is not None:
        last_result_data["last_result"] = new_result
        FileTools.write_json_file("lastResult.json", last_result_data)

    if no_repeat:
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

        FileTools.write_json_file(already_randomized_path, already_randomized_data)

if __name__ == "__main__":
    FileTools.create_template_file("lastResult.json", {})
    FileTools.create_template_file("listToRandomize.json", {
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]})
    if "--loop" in [arg.lower() for arg in sys.argv]:
        flag_index = [arg.lower() for arg in sys.argv].index("--loop")
        value_index = flag_index + 1
        if value_index < len(sys.argv):
            value = sys.argv[value_index]
        else:
            print_color("ERROR", "red")
            raise ValueError("no value provided after the '--loop' flag.")

        if value.isdigit():
            for i in range(int(value)):
                main()
        else:
            print_color("ERROR", "red")
            raise ValueError("no valid integer value for the '--loop' flag.")
    else:
        main()
