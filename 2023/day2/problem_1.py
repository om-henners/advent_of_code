from collections import defaultdict, UserDict
import re


GAME_MATCH = re.compile(r"""Game (\d+)""")
GRAB_MATCH = re.compile(r"""(\d+) (\w+)""")


class Marbles(UserDict):

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return 0

    def __setitem__(self, key, newvalue):
        super().__setitem__(key, max(newvalue, self[key]))

    @property
    def possible(self):
        return self["red"] <= 12 and self["green"] <= 13 and self["blue"] <= 14


games = defaultdict(Marbles)

for line in open("input"):
    game, grabs = line.split(":", 1)

    m = GAME_MATCH.match(game)
    game_id = int(m.group(1))

    for grab in GRAB_MATCH.findall(grabs):
        games[game_id][grab[1]] = int(grab[0])


print(sum(k for k, m in games.items() if m.possible))
