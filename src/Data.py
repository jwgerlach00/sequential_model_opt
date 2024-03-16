from typing import Callable, Dict, Optional, Union, Any, List

from src.Row import Row
from src.Cols import Cols
from src import utils


class Data:
    def __init__(
        self, src: Union[str, Dict[int, Any]], func: Optional[Callable] = None
    ) -> None:
        self.rows: Dict[int, "Row"] = {}
        self.cols: Optional["Cols"] = None

        self.adds(src, func)

    def adds(self, src: Union[str, Dict[int, Any]], func: Optional[Callable]):
        if type(src) == str:
            for _, value in utils.csv(src):
                self.add(value, func)
        else:
            for value in src.values():
                self.add(value, func)
        return self

    def add(self, t: Dict[int, Any], func: Callable) -> None:
        row = t if hasattr(t, "cells") else Row(t)

        if not self.cols:  # if header line
            self.cols = Cols(row)
            return
        else:  # if not header line
            if func:
                func(self, row)
            self.cols.add(row)
            self.rows[len(self.rows)] = row

    def mid(
        self, cols: Optional[List[str]], append_to: Optional[Dict[int, float]] = None
    ) -> "Row":
        u = append_to if append_to else {}

        for col in cols:
            u[len(u)] = self.cols.all[col].mid()
        return Row(u)

    def div(
        self, cols: Optional[List[str]], append_to: Optional[Dict[int, float]] = None
    ) -> "Row":
        u = append_to if append_to else {}

        for col in cols:
            u[len(u)] = self.cols.all[col].div()
        return Row(u)

    def mid_stats(self, digits: int = 2):
        u = {".N": len(self.rows)}

        for col in self.cols.y.values():
            u[col.txt] = round(col.mid(), digits)
        return u
