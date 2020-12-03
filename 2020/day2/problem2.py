import re
from operator import xor


password_pattern = re.compile(r"^(\d+)-(\d+) (.): (.+)$", re.M)


valid_count = 0


for match in password_pattern.finditer(open('input').read()):
    word = match.group(4)
    first = int(match.group(1)) - 1
    second = int(match.group(2)) - 1
    letter = match.group(3)

    if xor(word[first] == letter, word[second] == letter):
        valid_count += 1

print(valid_count)
