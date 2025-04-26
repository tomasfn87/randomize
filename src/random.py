from tools.color import print_color
from random import choice

class Random:
    def __init__(self, result_description, options, last_result):
        self.result_description = result_description
        self.options            = options
        self.last_result        = last_result

    def randomizer(self, total_options, position, no_repeat, cycle_count):

        description = self.result_description

        options = [name for name in self.options if name != self.last_result]
        if options:
            random_result = choice(options)
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
