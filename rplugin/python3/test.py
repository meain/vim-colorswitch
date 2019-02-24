from itertools import permutations
from .colorswitch import format_color


tests = [
    {"hex": "#000000", "rgb": "rgb(0.0, 0.0, 0.0)", "hsl": "hsl(0.0, 0.0, 0.0)"},
    {"hexa": "#ff0000e0", "rgba": "rgba(1.0, 0.0, 0.0, 0.88)", "hsla": "hsla(0.0, 1.0, 0.5, 0.88)"},
]

for test in tests:
    com = list(permutations(test.keys(), 2))
    for c in com:
        assert format_color(test[c[0]], c[1]) == test[c[1]]
