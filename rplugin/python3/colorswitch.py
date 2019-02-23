import re
import pynvim
from colour import Color


COLOR_FORMATS = ["hex", "rgb", "rgba", "hsl"]


def find_color_string(line: str):
    re_match = re.search(r"#[0-9a-f]*", line)
    if re_match:
        return "hex", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    re_match = re.search(r"rgb\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line)
    if re_match:
        return "rgb", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    re_match = re.search(
        r"rgba\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line
    )
    if re_match:
        return "rgba", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]

    re_match = re.search(r"hsl\(\ *\d*.?\d*\ *,\ *\d*.?\d*\ *,\ *\d*.?\d*\ *\)", line)
    if re_match:
        return "hsl", re_match.span(), line[re_match.span()[0] : re_match.span()[1]]
    return None, None, None


def get_color_object(color: str):
    if color.startswith("rgb("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        color_object = Color(rgb=clr)
    elif color.startswith("rgba("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        clr = clr[:-1]
        color_object = Color(rgb=clr)
    elif color.startswith("hsl("):
        clr = color[color.find("(") + 1 : color.find(")")]
        clr = clr.split(",")
        color_object = Color(hsl=clr)
    elif color.startswith("#"):
        color_object = Color(color)
    return color_object


def get_color_type(color: str):
    if color.startswith("rgb(") or color.startswith("rgba("):
        return "rgb"
    elif color.startswith("hsl("):
        return "hsl"
    elif color.startswith("#"):
        return "hex"
    else:
        return None


def simplify_color_values(values):
    values = list(values)
    for i in range(len(values)):
        values[i] = round(values[i], 2)
    return tuple(values)


def format_color(color, to: str = "hex") -> str:
    if isinstance(color, str):
        color = get_color_object(color)
    if to == "hsl":
        return "hsl" + str(simplify_color_values(color.hsl))
    elif to == "rgb":
        return "rgb" + str(simplify_color_values(color.hsl))
    elif to == "rgba":
        return "rgba" + str(simplify_color_values(tuple(list(color.hsl) + [1.0])))
    return color.hex


def switch_color(line: str):
    ctype, span, string = find_color_string(line)
    if ctype is None:
        return line
    totype = COLOR_FORMATS[(COLOR_FORMATS.index(ctype) + 1) % 4]
    newline = line[0 : span[0]] + format_color(string, totype) + line[span[1] :]
    return newline


@pynvim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @pynvim.function("ColorSwap", sync=True)
    def colorSwap(self, args):
        line = self.vim.current.line
        self.vim.current.line = switch_color(line)
