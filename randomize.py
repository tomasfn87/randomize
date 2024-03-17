from colorama import Fore, Style
from datetime import datetime as dt
import json
import os
import random
import re
import sys

def read_json_file(file_path, default_content=None):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return default_content
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def create_template_file(file_path, template_content):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        write_json_file(file_path, template_content)

def deduplicate(strings):
    unique_strings = set()
    deduplicated_list = []
    for string in strings:
        normalized_string = re.sub(
            r"[^a-zA-Z0-9À-ÿ]", "", " ".join(string.lower().split()))
        if normalized_string not in unique_strings:
            deduplicated_list.append(string)
            unique_strings.add(normalized_string)
    return deduplicated_list

def join_text(item_list, separator_1=" and ", separator_2=", "):
    assert isinstance(separator_1, str) and isinstance(separator_2, str)
    text = ""
    for i in range(0, len(item_list)):
        text += str(item_list[i])
        if i == len(item_list) - 1:
            return text
        elif i == len(item_list) - 2:
            text += separator_1
        else:
            text += separator_2

def print_color(text, color, end="\n"):
    if not type(text) == str:
        text = str(text)

    color_map = {
        "dim"         : Style.DIM,
        "green"       : Fore.GREEN,
        "red"         : Fore.LIGHTRED_EX,
        "yellow"      : Fore.YELLOW,
        "light blue"  : Fore.LIGHTBLUE_EX,
        "light yellow": Fore.LIGHTYELLOW_EX,
        "light green" : Fore.LIGHTGREEN_EX,
        "light cyan"  : Fore.LIGHTCYAN_EX}

    if color not in color_map:
        err = "Invalid color. Use "
        err += join_text(list(color_map.keys()), " or ") + "."
        raise ValueError(err)

    print(color_map[color] + text + Style.RESET_ALL, end=end)

def fix_file(file_name):
    print("Please edit file", end=" ")
    print_color(file_name.strip(), "yellow", end=" ")
    print("before continuing.")

def randomizer(
    options, result_to_avoid, result_description,
    total_options, position, no_repeat, cycle_count):

    description = result_description.capitalize()

    options = [name for name in options if name != result_to_avoid]
    if options:
        random_result = random.choice(options)
        print(f"{description}:\n- ",  end="")
        if no_repeat and position == total_options:
            if cycle_count % 2 == 0:
                print_color(random_result.strip(), "light green", end="")
            else:
                print_color(random_result.strip(), "green", end="")
        elif cycle_count % 2 == 0:
            print_color(random_result.strip(), "light cyan", end="")
        else:
            print_color(random_result.strip(), "light blue", end="")
        if no_repeat:
            print(" (", end="")
            if position == total_options:
                print_color(position, "light green", end="")
            else:
                print_color(position, "yellow", end="")
            print("/", end="")
            if position == total_options:
                print_color(total_options, "light green", end="")
            else:
                print_color(total_options, "light yellow", end="")
            print(")", end="")
        print()
        if random_result is not None:
            return random_result
    else:
        print("All options were selected. Let's start next round!")
        return None

def main():
    no_repeat = False
    if len(sys.argv) >= 2 and sys.argv[1].lower() == "--no-repeat":
        no_repeat = True

    last_result_data = read_json_file("lastResult.json", default_content={})
    list_to_randomize_data = read_json_file(
        "listToRandomize.json", default_content={
            "result_description": "my next trip will be to",
            "options": ["Portugal", "Spain", "France", "Italy"]})

    result_description = list_to_randomize_data.get(
        "result_description", "")

    options = list_to_randomize_data.get("options", [])
    check_options = deduplicate(options)

    if len(check_options) < len(options):
        print_color("ERROR", "red", end="")
        print(": duplicated options were detected.")
        fix_file("listToRandomize.json")
        return

    if len(options) < 2:
        print_color("ERROR", "red", end="")
        if len(options) == 1:
            print(": the only option is:", end=" ")
            print_color(options[0], "light yellow", end="")
            print(".")
        else:
            print(": no options were defined.")
        fix_file("listToRandomize.json")
        return

    if not result_description:
        print_color("ERROR", "red", end="")
        print(": invalid result description. Please check file ", end="")
        print_color("listToRandomize.json", "yellow", end="")
        print(".")
        return

    already_randomized_data = ""
    if no_repeat:
        already_randomized_path = "alreadyRandomized.json"

        if os.path.exists(already_randomized_path):
            already_randomized_data = read_json_file(
                already_randomized_path, default_content={
                    "all_options_randomized_count": 0,
                    "already_randomized": []})
        else:
            create_template_file(already_randomized_path, {
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

    new_result = randomizer(
        options            = options,
        result_to_avoid    = last_result,
        result_description = result_description,
        total_options      = total_options,
        position           = position,
        no_repeat          = no_repeat,
        cycle_count        = all_options_randomized_count)

    if new_result is not None:
        last_result_data["last_result"] = new_result
        write_json_file("lastResult.json", last_result_data)

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

        write_json_file(already_randomized_path, already_randomized_data)

if __name__ == "__main__":
    create_template_file("lastResult.json", {})
    create_template_file("listToRandomize.json", {
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]})
    main()
