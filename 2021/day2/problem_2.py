import re


pattern = re.compile(r"(forward|up|down) (\d+)")


text = open('input').read()


x, z, aim = 0, 0, 0

for match in pattern.finditer(text):

    val = int(match.group(2))

    if match.group(1) == 'forward':
        x += val
        z += val * aim
    elif match.group(1) == 'down':
        aim += val
    elif match.group(1) == 'up':
        aim -= val


print(x, z, x * z)
