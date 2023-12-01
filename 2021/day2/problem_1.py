import re


pattern = re.compile(r"(forward|up|down) (\d+)")


text = open('input').read()


x, z = 0, 0

for match in pattern.finditer(text):

    if match.group(1) == 'forward':
        x += int(match.group(2))
    elif match.group(1) == 'down':
        z += int(match.group(2))
    elif match.group(1) == 'up':
        z -= int(match.group(2))


print(x, z, x * z)
