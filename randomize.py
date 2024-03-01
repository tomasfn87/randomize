import json
import random
import os
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

def randomizer(options, result_to_avoid, result_description):
    options = [name for name in options if name != result_to_avoid]
    if options:
        random_result = random.choice(options)
        print(f"{result_description.capitalize()}:\n- {random_result}")
        return random_result
    else:
        print("No valid options to randomize.")
        return None

def main():
    no_repeat = False
    if len(sys.argv) >= 2 and sys.argv[1].lower() == '--no-repeat':
        no_repeat = True

    last_result_data = read_json_file('lastResult.json', default_content={})
    list_to_randomize_data = read_json_file('listToRandomize.json', default_content={
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]
    })

    options = list_to_randomize_data.get('options', [])

    if no_repeat:
        already_randomized_path = 'alreadyRandomized.json'

        if os.path.exists(already_randomized_path):
            already_randomized_data = read_json_file(already_randomized_path, default_content={
                "all_options_randomized_count": 0,
                "already_randomized": []
            })
        else:
            create_template_file(already_randomized_path, {
                "all_options_randomized_count": 0,
                "already_randomized": []
            })
            already_randomized_data = {
                "all_options_randomized_count": 0,
                "already_randomized": []
            }

        if already_randomized_data is not None:
            all_options_randomized_count = already_randomized_data.get('all_options_randomized_count', 0)
            already_randomized = already_randomized_data.get('already_randomized', [])

            if set(already_randomized) == set(options):
                already_randomized_data['already_randomized'] = []
                already_randomized_data['all_options_randomized_count'] += 1
                all_options_randomized_count = already_randomized_data['all_options_randomized_count']

                write_json_file(already_randomized_path, already_randomized_data)
            
            print(f"Times the whole list was run: {all_options_randomized_count}\n")

    result_description = list_to_randomize_data.get('result_description', None)

    if result_description is None or not options:
        print("Invalid configuration. Please check 'listToRandomize.json'.")
        return

    last_result = last_result_data.get('last_result')

    result_to_avoid = last_result
    if no_repeat and already_randomized_data is not None:
        options = [name for name in options if name not in already_randomized]

    new_result = randomizer(options, result_to_avoid, result_description)

    if new_result is not None:
        last_result_data['last_result'] = new_result
        write_json_file('lastResult.json', last_result_data)

        if no_repeat and already_randomized_data is not None:
            already_randomized_data['already_randomized'].append(new_result)
            write_json_file('alreadyRandomized.json', already_randomized_data)

if __name__ == "__main__":
    create_template_file('lastResult.json', {})
    create_template_file('listToRandomize.json', {
        "result_description": "my next trip will be to",
        "options": ["Portugal", "Spain", "France", "Italy"]
    })
    main()