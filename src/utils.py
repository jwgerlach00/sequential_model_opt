import fileinput, re, ast
import math
from typing import Any, Iterator, Tuple, List


# Reference: https://discord.com/channels/1191838787219759154/1192507528882438247/1195863830136377345
# Returns the values in the next row of the CSV as a list along with the row number of the next
def csv(filename: str = "-") -> Iterator[Tuple[int, List[Any]]]:
    i = 0
    with fileinput.FileInput(None if filename == "-" else filename) as src:
        for line in src:
            line = re.sub(r'([\n\t\r"\' ]|#.*)', "", line)
            if line:
                i += 1
                yield i, [coerce(x) for x in line.split(",")]


def output(d: dict) -> str:
    items = ", ".join([f"{k}: {v}" for k, v in sorted(d.items()) if k[0] != "_"])
    return f"{{{items}}}"


def coerce(s: str) -> Any:
    # Converts string rep to python datatype
    try:
        return ast.literal_eval(s)
    except Exception:
        return s.strip()


def sort_by_d2h(rows: dict, data) -> dict:
    return {
        i: val
        for i, val in zip(
            range(len(rows)),
            sorted(rows.values(), key=lambda row: row.d2h(data)),
        )
    }


# def slice(t: list, go: int = None, stop: int = None, inc: int = None) -> list:
#     go = go or 0
#     stop = stop or len(t)
#     inc = inc or 1

#     if go < 0:
#         go += len(t)
#     if stop < 0:
#         stop += len(t)

#     return t[go:stop:inc]


# def output_gate20_info(info):
#     for i, (k, v) in enumerate(info.items()):
#         for t in v:
#             print(f"{i + 1}. {k:<5} {pad_numbers(t)}")
#         print()


# def pad_numbers(t):
#     s = ""
#     if isinstance(t[0], list):
#         s = f"[{', '.join([f'{pad_numbers(v)}' for v in t])}]"
#     else:
#         s = f"[{', '.join([f'{v:5.2f}' for v in t])}]"
#     return s


# def align_list(lst, precision=2, pad=15):
#     out = "["
#     for i, cell in enumerate(lst):
#         if isinstance(cell, (int, float)):
#             cell = cell if int(cell) == cell else round(cell, precision)
#         if isinstance(cell, str):
#             cell = f"'{cell}'"
#         out += f"{str(cell):{pad if i < (len(lst) - 1) else 0}}"
#     out += "]"
#     return out


# def any(t):
#     return random.choice(t)


# def many(t, n):
#     if n == None:
#         n = len(t)

#     u = []
#     for i in range(n):
#         u.append(any(t))

#     return u
