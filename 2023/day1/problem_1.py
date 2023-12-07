import re


DIGET_FILTER = re.compile(r"\D")


total = 0

for line in open("input", "rt"):
    digits = DIGET_FILTER.sub("", line)
    number = int(digits[0] + digits[-1])
    total += number

print(total)
