text = open('input').read().split('\n\n')

groups = []

for g in text:
    persons = [set(p) for p in g.split()]
    if len(persons) > 1:
        groups.append(len(persons[0].intersection(*persons[1:])))
    else:
        groups.append(len(persons[0]))


print(sum(groups))
