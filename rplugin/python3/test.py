from itertools import permutations
from .colorswitch import format_color


tests = [
    {
        "hexa": "#ff0000e0",
        "rgba": "rgba(255, 0, 0, 0.88)",
        "hsla": "hsla(0, 100%, 50%, 0.88)",
    },
    {
        "hex": "#ff0000",
        "rgb": "rgb(255, 0, 0)",
        "hsl": "hsl(0, 100%, 50%)",
    },
    # {
    #     "hexa": "#3d5c3fea",
    #     "rgba": "rgba(61, 91, 63, 0.92)",
    #     "hsla": "hsla(122, 20%, 30%, 0.92)",
    # },
]

for test in tests:
    com = list(permutations(test.keys(), 2))
    for c in com:
        assert format_color(test[c[0]], c[1]) == test[c[1]]
