import re
import string


pattern = '(' + '|'.join(
    f'{l}{u}|{u}{l}'
    for l, u in zip(string.ascii_lowercase, string.ascii_uppercase)
    ) + ')'
pattern = re.compile(pattern)

input_text = open('input.txt').read().strip()


def react_polymer(polymer):
    num_matches = len(polymer)
    out_string = polymer

    while num_matches > 0:
        out_string, num_matches = pattern.subn('', out_string)

    return len(out_string)


broken_letter = {}
for letter in string.ascii_lowercase:
    print(letter)
    polymer = re.sub(letter, '', input_text, flags=re.I)
    broken_letter[letter] = react_polymer(polymer)

l = min(broken_letter, key=broken_letter.get)
print(l, broken_letter[l])
