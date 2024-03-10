from datetime import datetime as dt
import json
import os
import random
import sys

def read_json_file(file_path, default_content=None):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return default_content
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def create_template_file(file_path, template_content):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        write_json_file(file_path, template_content)

def randomizer(
    options, result_to_avoid, result_description, total_options, no_repeat):

    position = total_options - len(options) + 1
    description = result_description.capitalize()

    options = [name for name in options if name != result_to_avoid]
    if options:
        random_result = random.choice(options)
        print(f"{description}:\n- {random_result}", end="")
        if no_repeat:
            print(f" ({position}/{total_options})", end="")
        print()
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
            if already_randomized:
                i = all_options_randomized_count
                if already_randomized[i]["selected"]:
                    actual_options = already_randomized[i]["selected"]

            if set(actual_options) == set(options):
                already_randomized_data['all_options_randomized_count'] += 1
                all_options_randomized_count += 1
                actual_options = []

                write_json_file(
                    already_randomized_path, already_randomized_data)

            print(
                f"Times list was completed: {all_options_randomized_count}\n")

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

    new_result = randomizer(
        options, result_to_avoid, result_description,
        total_options, no_repeat)

    if new_result is not None:
        last_result_data['last_result'] = new_result
        write_json_file('lastResult.json', last_result_data)

    if no_repeat:
        i = all_options_randomized_count
        if len(already_randomized) < i + 1:
            already_randomized_data['already_randomized'].append({
                "datetime": str(dt.now())[0:19],
                "comments": "", "selected": []})
        already_randomized_data['already_randomized'][i]["selected"] \
            .append(new_result)

        write_json_file('alreadyRandomized.json', already_randomized_data)

if __name__ == "__main__":
    create_template_file('lastResult.json', {})
    create_template_file('listToRandomize.json', {
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]})
    main()
