from random import randint
from re import findall, search

POSSIBLE_DICES = tuple(f"D{_}" for _ in (3, 4, 6, 8, 10, 12, 20, 100))


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
    elif code[-1] in ("+" , "-"):
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
    tmp = findall("D", code)
    if len(tmp) == 0:
        return "No dice specified!"
    elif len(tmp) > 1:
        return "Only one 'D' is allowed!"
    else:
        x = search(r"(\d*)D", code).group(1)
        x = 1 if not x else int(x)
        y = int(search(r"D(\d+)", code).group(1))
        if f"D{y}" not in POSSIBLE_DICES:
            return f"Not allowed dice: D{y}"
    if search("[\+\-]\d*D", code):
        return "Wrong dice code!"
    tmp = findall("[\+\-]", code)
    if len(tmp) > 1:
        return "Only one modifier is allowed!"
    elif len(tmp) == 0:
        z = 0
    else:
        z = search(r"[\+\-](\d+)", code)
        if not z:
            return f"No value after '{code[-1]}'!"
        if z.group(0)[0] == '+':
            z = int(z.group(1))
        else:
            z = 0 - int(z.group(1))
    return sum([randint(1, y) for _ in range(x)]) + z


if __name__ == "__main__":
    test_codes = (("2D10+10", "D6", "2D3", "D12-1", "5D8-4",
                   "2D10-1", "2D10+10", "D6", "2D3", "D12-1",
                   "32D3-", "DD34", "4-3D6", "+D10", "",
                   "2D6+1+2", "2D10-10+1", "7D7+7", "2d8", "D8*2"))
    for c in test_codes:
        print(roll_the_dice(c), end=" | ")
        print(roll_the_dice_re(c))

