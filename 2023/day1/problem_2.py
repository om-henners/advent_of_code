import re


TEXT_DIGITS = {
    "one": "o1e",
    "two": "t2o",
    "three": "th3ee",
    "four": "fo4ur",
    "five": "fi5ve",
    "six": "s6x",
    "seven": "se7en",
    "eight": "ei8ht",
    "nine": "ni9ne",
}
DIGET_FILTER = re.compile(r"\D")


total = 0

for line in open("input", "rt"):
    for text_digit, repl in TEXT_DIGITS.items():
        line = line.replace(text_digit, repl)
    digits = DIGET_FILTER.sub("", line)
    number = int(digits[0] + digits[-1])
    total += number

print(total)
