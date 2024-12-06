import re

mul = re.compile(r"""(?:mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))""")
data = open("input").read()


keep = []
bin = []


current = keep

for match in mul.finditer(data):
    if match.group(0) == "don't()":
        current = bin
    elif match.group(0) == "do()":
        current = keep
    else:
        current.append(int(match[1]) * int(match[2]))

print(sum(keep))
