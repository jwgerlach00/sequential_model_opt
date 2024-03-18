from typing import Callable, Dict, Optional, Union, Any, List, Tuple
from random import shuffle

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

    def __str__(self) -> str:
        # Initialize the string with column names
        s = "\t".join(self.cols.names) + "\n"

        # Iterate through rows and concatenate cell values
        for row in self.rows.values():
            s += "\t".join([str(x) for x in row.cells]) + "\n"

        return s

    def adds(self, src: Union[str, Dict[int, Any]], func: Optional[Callable]):
        if type(src) == str:
            for _, value in utils.csv(src):
                self.add(value, func)
        else:
            # for value in src.values():
            self.add(src, func)
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
        self, cols: Optional[List[int]], append_to: Optional[Dict[int, float]] = None
    ) -> "Row":
        u = append_to if append_to else {}
        cols = cols if cols else self.cols.all.keys()

        for col in cols:
            u[len(u)] = self.cols.all[col].mid()
        return Row(u)

    def div(
        self, cols: Optional[List[int]], append_to: Optional[Dict[int, float]] = None
    ) -> "Row":
        u = append_to if append_to else {}
        cols = cols if cols else self.cols.all.keys()

        for col in cols:
            u[len(u)] = self.cols.all[col].div()
        return Row(u)

    def mid_stats(self, digits: int = 2) -> dict:
        u = {".N": len(self.rows)}

        for col in self.cols.y.values():
            u[col.txt] = round(col.mid(), digits)
        return u

    def shuffle(self) -> None:
        # Only need to shuffle the rows, not the columns (SYM, NUM) because the columns
        # do not care about order

        # When you shuffle a dictionary with 0-n index keys it will work
        shuffle(self.rows)

    def gate(self, budget0: int, budget: int, lite_pow: float = 0.5) -> Tuple[dict, dict]:
        # Shuffle rows
        self.shuffle()

        stats = {}
        bests = {}

        lite = self.slice_rows(0, budget0)
        dark = self.slice_rows(budget0)  # budget0 to end

        for i in range(budget):
            best_data, rest_data = self.best_rest(lite, round((len(lite)) ** lite_pow))
            todo, selected = self.split(best_data, rest_data, lite, dark)
            print(f"todo: {todo}")
            stats[i] = selected.mid(None)
            bests[i] = best_data.rows[0]

            # Move 1 example from dark into lite
            lite[todo] = dark.pop(todo)
        
        return stats, bests

    def slice_rows(self, from_i: int, to_i: Optional[int] = None):
        out = {}

        for i in range(from_i, to_i if to_i else len(self.rows)):
            out[i] = self.rows[i]

        return out

    def best_rest(self, rows, n_best):
        rows = utils.sort_by_d2h(rows, self)

        best = Data(self.cols.names)
        rest = Data(self.cols.names)

        for row in rows.values():
            if n_best > 0:
                n_best -= 1
                best.add(row, None)
            else:
                rest.add(row, None)

        return best, rest

    def split(self, best_data, rest_data, lite_rows, dark_rows):
        selected = Data(self.cols.names)

        max_challenge_score = -1 * float("inf")  # arbitrarily small number
        out_index = 1

        for i, row in dark_rows.items():
            prob_belonging_to_best = row.like(best_data, len(lite_rows), 2)
            prob_belonging_to_rest = row.like(rest_data, len(lite_rows), 2)

            if prob_belonging_to_best > prob_belonging_to_rest:
                selected.add(row, None)

            challenge_score = abs(  # how well will this example be for learning?
                prob_belonging_to_best + prob_belonging_to_rest
            ) / (abs(prob_belonging_to_best - prob_belonging_to_best + 1e-30))

            if challenge_score > max_challenge_score:
                max_challenge_score = challenge_score
                out_index = i

        return out_index, selected
