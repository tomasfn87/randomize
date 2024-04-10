from colorama import Fore, Style
from tools.string_tools import StringTools

def print_color(text, color, end="\n"):
    if not type(text) == str:
        text = str(text)

    color_map = {
        "dim"         : Style.DIM,
        "red"         : Fore.LIGHTRED_EX,
        "yellow"      : Fore.YELLOW,
        "light blue"  : Fore.LIGHTBLUE_EX,
        "light yellow": Fore.LIGHTYELLOW_EX,
        "light green" : Fore.LIGHTGREEN_EX,
        "light cyan"  : Fore.LIGHTCYAN_EX}

    if color not in color_map:
        print()
        print_color("ERROR", "red")
        err = "invalid color. Use "
        err += StringTools.join_text(list(color_map.keys()), " or ") + "."
        raise ValueError(err)

    print(color_map[color] + text + Style.RESET_ALL, end=end)