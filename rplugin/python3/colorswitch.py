import re
from colour import Color
from importlib.util import find_spec

# from .utils import cycle_color
# from importlib import import_module
# utils = import_module('utils')

if find_spec("yarp"):
    import vim
elif find_spec("pynvim"):
    import pynvim

    vim = pynvim
else:
    import neovim

    vim = neovim


COLOR_FORMATS = {
    "without_alpha": ["hex", "rgb", "hsl"],
    "with_alpha": ["hexa", "rgba", "hsla"],
}
CSS_MODE = False


def find_color_string(line: str):
    # hex formats
    re_match = re.search(r"#[0-9a-f]{8}", line)
    if re_match:
        return "hexa", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]
    re_match = re.search(r"#[0-9a-f]{6}", line)
    if re_match:
        return "hex", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]
    re_match = re.search(r"#[0-9a-f]{3}", line)
    if re_match:
        return "hex", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    # rgb formats
    re_match = re.search(r"rgb\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line)
    if re_match:
        return "rgb", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    re_match = re.search(
        r"rgba\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line
    )
    if re_match:
        return "rgba", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    # hsl formats
    re_match = re.search(r"hsl\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line)
    if re_match:
        return "hsl", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]
    re_match = re.search(
        r"hsla\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line
    )
    if re_match:
        return "hsla", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    return None, None, None


def get_color_object(color: str):
    alpha = 1.0
    if color.startswith("rgb("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        color_object = Color(rgb=clr)
    elif color.startswith("rgba("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        alpha = clr[-1]
        clr = clr[:-1]
        color_object = Color(rgb=clr)

    elif color.startswith("hsl("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        color_object = Color(hsl=clr)
    elif color.startswith("hsla("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        alpha = clr[-1]
        clr = clr[:-1]
        color_object = Color(hsl=clr)

    elif color.startswith("#"):
        if len(color) == 4 or len(color) == 7:
            color_object = Color(color)
        elif len(color) == 9:
            color_object = Color(color[:-2])
            alpha = int(color[-2:], 16) / 100
    return color_object, alpha


def simplify_color_values(values):
    values = list(values)
    for i in range(len(values)):
        values[i] = round(float(str(values[i]).strip()), 2)
    return tuple(values)


def _get_hex_alpha(value=int):
    str_value = str(hex(int(float(str(value).strip()) * 100)))[2:]
    if len(str_value) == 1:
        str_value = "0" + str_value
    return str_value


def format_color(color, to: str = "hex") -> str:
    if isinstance(color, str):
        color, alpha = get_color_object(color)
    if to == "hsl":
        return "hsl" + str(simplify_color_values(color.hsl))
    elif to == "hsla":
        return "hsla" + str(simplify_color_values(tuple(list(color.rgb) + [alpha])))

    elif to == "rgb":
        return "rgb" + str(simplify_color_values(color.rgb))
    elif to == "rgba":
        return "rgba" + str(simplify_color_values(tuple(list(color.rgb) + [alpha])))
    elif to == "hexa":
        return color.hex_l + _get_hex_alpha(alpha)
    return color.hex_l


def cycle_color(line: str):
    ctype, span, string = find_color_string(line)
    if ctype is None:
        return line
    if ctype[-1] == "a":
        cl = COLOR_FORMATS["with_alpha"]
        totype = cl[(cl.index(ctype) + 1) % len(cl)]
    else:
        cl = COLOR_FORMATS["without_alpha"]
        totype = cl[(cl.index(ctype) + 1) % len(cl)]
    newline = line[0 : span[0]] + format_color(string, totype) + line[span[1] :]
    return newline


@vim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @vim.function("ColorSwap", sync=True)
    def colorSwap(self, args):
        line = self.vim.current.line
        self.vim.current.line = cycle_color(line)
