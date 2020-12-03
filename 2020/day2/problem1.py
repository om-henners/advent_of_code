import re
from collections import Counter


password_pattern = re.compile(r"^(\d+)-(\d+) (.): (.+)$", re.M)


valid_count = 0


for match in password_pattern.finditer(open('input').read()):
    counts = Counter(match.group(4))
    if int(match.group(1)) <= counts[match.group(3)] <= int(match.group(2)):
           valid_count += 1

print(valid_count)
