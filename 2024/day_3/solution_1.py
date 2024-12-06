import re


mul = re.compile(r"""mul\((\d{1,3}),(\d{1,3})\)""")

data = open("input").read()


results = []
for match in mul.findall(data):
    results.append(int(match[0]) * int(match[1]))

print(sum(results))
