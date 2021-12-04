text = open('input').read().split('\n\n')

groups = []

for g in text:
    g = g.replace('\n', '')
    groups.append(len(set(g)))

print(sum(groups))
