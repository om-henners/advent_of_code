import re

validations = {
    'byr': re.compile(r'(19[2-9]\d|200[0-2])(?!\S)'),
    'iyr': re.compile(r'(20(?:1\d|20))(?!\S)'),
    'eyr': re.compile(r'(20(?:2\d|30))(?!\S)'),
    'hgt': re.compile(r'(1(?:[5-8]\d|9[0-3])cm|59in|6\din|7[0-6]in)(?!\S)'),
    'hcl': re.compile(r'#[0-9a-f]{6}(?!\S)'),
    'ecl': re.compile(r'(amb|blu|brn|gry|grn|hzl|oth)(?!\S)'),
    'pid': re.compile(r'\d{9}(?!\S)')
}

with open('input') as f:
    text = f.read()

passports = text.split('\n\n')


fields = re.compile('(\w{3}):')

fails = 0

for p in passports:
    count = []
    for chunk in p.split():
        word = chunk[:3]
        if word not in validations:
            print(word)
            continue
        if not validations[word].match(chunk[4:]):
            print(word, validations[word], chunk[4:])
            print(p, '\n')
            fails += 1
            break
        else:
            count.append(word)
    else:
        if len(count) != len(validations) or not set(count).issubset(validations.keys()):
            print('count failed', len(count), count)
            print(p.split(), '\n')
            fails += 1


print(fails, len(passports), len(passports) - fails)
