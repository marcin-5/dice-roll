from random import randint
from re import findall, match, search

POSSIBLE_DICES = tuple(f"D{_}" for _ in (3, 4, 6, 8, 10, 12, 20, 100))


def add_return_var(func):
    """When function returns error message add param from function call to the message."""
    def wrapper(var):
        res = func(var)
        if type(res) is str:
            res += f" [{str(var)}]"
        return res
    return wrapper


@add_return_var
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
        return f"No value after '{code[-1]}'!"
    for i in POSSIBLE_DICES:
        if i in code:
            break
    else:
        y = code.split("D")[1]
        if "+" in y:
            y = y.split("+")[0]
        elif "-" in y:
            y = y.split("-")[0]
        return f"Not allowed dice: D{y}"
    if code[0] == "D":
        x = 1
    else:
        x = ""
        while not code[0] == "D":
            if code[0] in ("+", "-"):
                return "Wrong dice code!"
            x += code[0]
            code = code[1:]
        x = int(x)
    code = code[1:]
    if "+" in code:
        y, z = code.split("+")
        y = int(y)
        z = int(z)
    elif "-" in code:
        y, z = code.split("-")
        y = int(y)
        z = 0 - int(z)
    else:
        y = int(code)
        z = 0
    return sum([randint(1, y) for _ in range(x)]) + z


def split_dice_code(code):
    """Return x, y, z from dice code xDy+z"""
    if not code:
        return '', '', ''   # empty code
    try:
        return match("(.*)D([^\+\-]*)([\+\-]?.*)", code).group(1, 2, 3)
    except AttributeError:
        return '', '', ''   # no D in code


@add_return_var
def roll_the_dice_re(code):
    """
    Calculate dice roll from dice pattern.
    (version with regular expressions)

    :param str code: dice pattern ex. `7D12-5`
    :rtype: int, str
    :return: dice roll value for proper dice pattern, error message elsewhere
    """
    tmp = search("([^\+\-\dD])", code)
    if tmp:
        return "Not allowed char: " + tmp.group(0)
    x, y, z = split_dice_code(code)
    if not y:
        return "No dice specified!"
    elif "D" + y not in POSSIBLE_DICES:
        return f"Not allowed dice: D{y}!"
    else:
        y = int(y)
    if "D" in x:
        return "Only one 'D' is allowed!"
    elif "+" in x or "-" in x:
        return "Wrong dice code!"
    elif not x:
        x = 1
    else:
        x = int(x)
    if not z:
        z = 0
    else:
        if len(findall("[\+\-]", z)) > 1:
            return "Only one modifier is allowed!"
        elif z in ("+", "-"):
            return f"No value after '{z}'!"
        else:
            z = int(z)
    return sum([randint(1, y) for _ in range(x)]) + z


if __name__ == "__main__":
    test_codes = (("2D10+10", "D6", "2D3", "D12-1", "5D8-4",
                   "2D10-1", "2D10+10", "D6", "2D3", "D12-1",
                   "32D3-", "DD34", "4-3D6", "+D10", "", "2+2",
                   "2D6+1+2", "2D10-10+1", "7D7+7", "2d8", "D8*2"))
    for c in test_codes:
        print(roll_the_dice(c), end=" | ")
        print(roll_the_dice_re(c))
