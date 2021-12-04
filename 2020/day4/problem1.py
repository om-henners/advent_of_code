import re

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

with open('input') as f:
    text = f.read()

passports = text.split('\n\n')


fields = re.compile('(\w{3}):')

count = 0

for p in passports:
    if required_fields.issubset(set(fields.findall(p))):
        count += 1

print(count)
