import re
import string


match_pattern = '(' + '|'.join(
    f'{l}{u}|{u}{l}'
    for l, u in zip(string.ascii_lowercase, string.ascii_uppercase)
    ) + ')'
print(match_pattern)


pattern = re.compile(match_pattern)

input_text = open('input.txt').read().strip()


num_matches = len(input_text)
out_string = input_text

while num_matches > 0:
    out_string, num_matches = pattern.subn('', out_string)

print(out_string, len(out_string))
