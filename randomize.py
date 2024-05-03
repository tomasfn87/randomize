from src.random_session import RandomSession
from sys import argv
from tools.color import print_color


def main():
    no_repeat = False
    if "--no-repeat" in [arg.lower() for arg in argv]:
        no_repeat = True

    random_session = RandomSession(
        list_to_randomize  = "listToRandomize.json",
        last_result        = "lastResult.json",
        already_randomized = "alreadyRandomized.json",
        no_repeat          = no_repeat)

    if "--loop" in [arg.lower() for arg in argv]:
        flag_index = [arg.lower() for arg in argv].index("--loop")
        value_index = flag_index + 1
        if value_index < len(argv):
            value = argv[value_index]
        else:
            print_color("ERROR", "red")
            raise ValueError("no value provided after the '--loop' flag.")
        if not value.isdigit():
            print_color("ERROR", "red")
            raise ValueError("no valid integer value for the '--loop' flag.")
        else:
            for i in range(int(value)):
                random_session.session()
    else:
        random_session.session()

if __name__ == '__main__':
    main()