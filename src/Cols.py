import re
from typing import Dict, Union, Optional

from src.Row import Row
from src.Num import Num
from src.Sym import Sym


class Cols:
    def __init__(self, row: "Row") -> None:
        self.x: Dict[int, Union["Num", "Sym"]] = {}
        self.y: Dict[int, Union["Num", "Sym"]] = {}
        self.all: Dict[int, Union["Num", "Sym"]] = {}
        self.klass: Optional[Union["Num", "Sym"]] = None
        self.names: dict = row.cells

        # Upper is Num column
        # lower is Sym column
        # __X is ignore
        # __! is class target
        # __+ is maximize target
        # __- is minimize target
        # __ is feature
        for at, col_name in enumerate(row.cells):
            # Num if col_name begins with an uppercase letter, else Sym
            col_class = Num if re.match(r"^[A-Z]", col_name) else Sym
            col = col_class(col_name, at)

            self.all[len(self.all)] = col

            if not re.match(r".*X$", col_name):  # if not "X" at end of col_name
                if re.match(
                    r".*!$", col_name
                ):  # if "!" at end of line, this is the target class
                    self.klass = col

                if re.match(
                    r".*[!+-]$", col_name
                ):  # if "!", "+", or "-" at end of col_name
                    self.y[at] = col  # Y, target
                else:
                    self.x[at] = col  # X, feature

    def add(self, row: "Row") -> "Row":
        for col in list(self.y.values()) + list(self.x.values()):
            # Add to Num or Sym column
            col.add(row.cells[col.at])
        return row
