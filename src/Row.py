from typing import Dict


class Row:
    def __init__(self, t: list) -> None:
        self.cells = t

    # def d2h(self, data: Data, d, n) -> float:
    #     d = 0
    #     n = 0

    #     for col in data.cols.y.values():
    #         n += 1
    #         d += abs(col.heaven - col.norm)
