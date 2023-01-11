from random import randint
import re

POSSIBLE_DICES = tuple(f"D{_}" for _ in (3, 4, 6, 8, 10, 12, 20, 100))


def add_arg_to_err_msg(func):
    """When function returns error message add param from function call to the message."""
    def wrapper(var):
        res = func(var)
        if type(res) is str:
            res += f" [{var}]"
        return res
    return wrapper


@add_arg_to_err_msg
def roll_the_dice(code):
    """
    Calculate dice roll from dice pattern.

    :param str code: dice pattern ex. `7D12-5`
    :rtype: int, str
    :return: dice roll value for proper dice pattern, error message elsewhere
    """
    exp_chars = tuple([str(_) for _ in range(0, 10)] + ["D", "+", "-"])
    for i in code:
        if i not in exp_chars:
            return f"Not allowed char: {i}"
    if "D" not in code:
        return "No dice specified!"
    elif code.count("D") > 1:
        return "Only one 'D' is allowed!"
    if (code.count("+") + code.count("-")) > 1:
        return "Only one modifier is allowed!"
    elif code[-1] in ("+", "-"):
        code += "0"
    for i in POSSIBLE_DICES:
        if i in code:
            break
    else:
        return f"Not allowed dice: D{code.split('D')[1].replace('-', '+').split('+')[0]}"
    x, code = code.split("D")
    if any(_ in x for _ in ("+", "-")):
        return "Wrong dice code!"
    x = int(x) if x else 1
    code = code.replace("+", "|+").replace("-", "|-")
    try:
        y, z = code.split("|")
        y = int(y)
        z = int(z)
    except ValueError:
        y = int(code)
        z = 0
    return sum([randint(1, y) for _ in range(x)]) + z


def split_dice_code(code):
    """Return x, y, z from dice code xDy+z"""
    if not code or "D" not in code:
        return '', '', ''   # empty code or not D in code
    return re.match("(.*)D([^\+\-]*)([\+\-]?.*)", code).group(1, 2, 3)


@add_arg_to_err_msg
def roll_the_dice_re(code):
    """
    Calculate dice roll from dice pattern.
    (version with regular expressions)

    :param str code: dice pattern ex. `7D12-5`
    :rtype: int, str
    :return: dice roll value for proper dice pattern, error message elsewhere
    """
    if m := re.search("([^\+\-\dD])", code):
        return "Not allowed char: " + m.group(0)
    match split_dice_code(code):
        case (x, y, z) if not y:
            return "No dice specified!"
        case (x, y, z) if "D" + y not in POSSIBLE_DICES:
            return f"Not allowed dice: D{y}!"
        case (x, y, z) if "D" in x:
            return "Only one 'D' is allowed!"
        case (x, y, z) if "+" in x or "-" in x:
            return "Wrong dice code!"
        case (x, y, z) if len(re.findall("[\+\-]", z)) > 1:
            return "Only one modifier is allowed!"
        case (x, y, z):
            y = int(y)
            x = int(x) if x else 1
            z = 0 if not z or z in ("+", "-") else int(z)
            return sum([randint(1, y) for _ in range(x)]) + z
        case _:
            return "FIXME"


def get_min_value(code):
    """Returns min value for dice code"""
    x, _, z = split_dice_code(code)
    x = int(x) if x else 1
    z = int(z) if z else 0
    return x * 1 + z


def get_max_value(code):
    """Returns max value for dice code"""
    x, y, z = split_dice_code(code)
    x = int(x) if x else 1
    y = int(y)
    z = int(z) if z else 0
    return x * y + z


if __name__ == "__main__":
    test_codes = (("2D10+10", "D6", "2D3", "D12-1", "5D8-4",
                   "2D10-1", "2D10+10", "D6", "2D3", "D12-1",
                   "32D3-", "DD34", "DD100", "4-3D6", "+D10",
                   "", "2+2", "2D6+1+2", "2D10-10+1", "2d8", "D8*2",
                   "7D7+7", "D1", "2D2"))
    for c in test_codes:
        print(roll_the_dice(c), end=" | ")
        print(roll_the_dice_re(c))

    test_min_max = {
        "D3-1": 0,
        "D4+1": 5,
        "3D6-3": 15,
        "6D8+7": 55,
        "5D10-4": 1,
        "2D12+1": 25,
        "11D3": 33,
        "8D4-7": 1
    }
    for c, v in test_min_max.items():
        r = roll_the_dice_re(c)
        while not r == v:
            print(c, v, r, " " * 10, end="\r")
            r = roll_the_dice_re(c)
        print(c, v, r, " " * 10)

    for c, v in test_min_max.items():
        rmin = get_min_value(c)
        rmax = get_max_value(c)
        for i in range(1000):
            r = roll_the_dice_re(c)
            if v == rmin or v == rmax:
                if r < rmin or r > rmax:
                    print("!", c, v, r)
                    break
            else:
                print(f"v not in ({rmin}, {rmax}) for {c} code.")
        else:
            print(f"All results for code {c} >= {rmin} and <= {rmax}")
