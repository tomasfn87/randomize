from datetime import datetime as dt
from colorama import Fore, Style
import json
import os
import random
import sys

def read_json_file(file_path, default_content=None):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return default_content
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def create_template_file(file_path, template_content):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        write_json_file(file_path, template_content)

def deduplicate(strings):
    unique_strings = set()
    deduplicated_list = []
    for string in strings:
        normalized_string = ' '.join(string.lower().split())
        if normalized_string not in unique_strings:
            deduplicated_list.append(string)
            unique_strings.add(normalized_string)
    return deduplicated_list

def print_color(text, color, end="\n"):
    if not type(text) == str:
        text = str(text)

    color_map = {
        'yellow': Fore.YELLOW,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'light blue': Fore.CYAN,}

    if color not in color_map:
        raise ValueError(
            "Invalid color. Use 'yellow', 'red', 'green' or 'light blue'.")

    print(color_map[color] + text + Style.RESET_ALL, end=end)

def fix_file(file_name):
    print("Please edit file", end=" ")
    print_color(file_name.strip(), "yellow", end=" ")
    print("before continuing.")

def randomizer(
    options, result_to_avoid, result_description,
    total_options, position, no_repeat):

    description = result_description.capitalize()

    options = [name for name in options if name != result_to_avoid]
    if options:
        random_result = random.choice(options)
        print(f"{description}:\n- ",  end="")
        print_color(random_result, "light blue", end="")
        if no_repeat:
            print(f" ({position}/{total_options})", end="")
        print()
        if random_result is not None:
            return random_result
    else:
        print("All options were selected. Let's start next round!")
        return None

def main():
    no_repeat = False
    if len(sys.argv) >= 2 and sys.argv[1].lower() == '--no-repeat':
        no_repeat = True

    last_result_data = read_json_file('lastResult.json', default_content={})
    list_to_randomize_data = read_json_file(
        'listToRandomize.json', default_content={
            "result_description": "my next trip will be to",
            "options": ["Portugal", "Spain", "France", "Italy"]})

    options = list_to_randomize_data.get('options', [])
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
            print_color(options[0], "light blue", end="")
            print(".")
        else:
            print(f": no options were defined.")
        fix_file("listToRandomize.json")
        return

    already_randomized_data = ""
    if no_repeat:
        already_randomized_path = 'alreadyRandomized.json'

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

        if already_randomized_data is not None:
            all_options_randomized_count = already_randomized_data.get(
                'all_options_randomized_count', 0)
            already_randomized = already_randomized_data.get(
                'already_randomized', [])

            actual_options = []
            if already_randomized and already_randomized[0]["selected"]:
                    actual_options = already_randomized[0]["selected"]

            if len(actual_options) >= len(options):
                actual_options = []

        if len(already_randomized) < all_options_randomized_count + 1:
            already_randomized_data['already_randomized'].insert(0, {
                "datetime": str(dt.now())[0:19],
                "comments": [], "selected": []})

    result_description = list_to_randomize_data.get(
        'result_description', None)

    if result_description is None or not options:
        print("Invalid configuration. Please check 'listToRandomize.json'.")
        return

    total_options = len(options)
    if no_repeat and actual_options:
        options = [name for name in options if name not in actual_options]

    last_result = last_result_data.get('last_result')
    result_to_avoid = last_result

    position = 0
    if no_repeat:
        position = len(
            already_randomized_data['already_randomized'][0]["selected"]) + 1

    new_result = randomizer(
        options, result_to_avoid, result_description,
        total_options, position, no_repeat)

    if new_result is not None:
        last_result_data['last_result'] = new_result
        write_json_file('lastResult.json', last_result_data)

    if no_repeat:
        already_randomized_data['already_randomized'][0]["selected"] \
            .append(new_result)
        if len(already_randomized_data['already_randomized'][0]["selected"]) \
            >= total_options:
            already_randomized_data['all_options_randomized_count'] = \
                len(already_randomized_data['already_randomized'])
            all_options_randomized_count += 1
            write_json_file(
                already_randomized_path, already_randomized_data)

        print(
            f"\nTimes list was completed: ", end="")
        if all_options_randomized_count == 0:
            print_color(all_options_randomized_count, "red")
        else:
            if all_options_randomized_count % 2 == 0:
                print_color(all_options_randomized_count, "yellow")
            else:
                print_color(all_options_randomized_count, "green")

        write_json_file('alreadyRandomized.json', already_randomized_data)

if __name__ == "__main__":
    create_template_file('lastResult.json', {})
    create_template_file('listToRandomize.json', {
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]})
    main()