import math
from src.config import config


class Row:
    def __init__(self, t: list) -> None:
        self.cells = t

    def likes(self, datas: dict, n: int):
        most = -1 * float("inf")
        best_class = None

        n_hypothesis = len(datas)

        for klass, data in datas.items():
            like_val = self.like(data, n, n_hypothesis)
            if like_val > most:
                best_class = klass
                most = like_val
        return best_class, most

    def like(self, data, n: int, n_hypothesis: int) -> float:
        # Using log addition rather than multiplication
        prior = (len(data.rows) + config.k) / (
            n + config.k * n_hypothesis
        )  # assuming data contains data for only one class, this is prior probability
        # where n is the length of all classes data

        out = math.log(prior)  # log for log sum rather than multiplication
        # this helps in small frequency math

        for col in data.cols.x.values():
            v = self.cells[col.at]
            if v != "?":  # if value is not missing
                inc = col.like(v, prior)
                out += math.log(inc) if inc > 0 else 0  # log again for small frequency
        return math.e**out  # undo logs

    def d2h(self, data) -> float:
        # euclidean distance
        d = 0
        n = 0

        for y_col in data.cols.y.values():
            n += 1
            d += (
                y_col.heaven - y_col.norm(self.cells[y_col.at])
            ) ** 2  # square the difference (no need for abs bc squared)

        return d**0.5 / n**0.5  # divide by n to normalize

    # def d2h(self, data: Data, d, n) -> float:
    #     d = 0
    #     n = 0

    #     for col in data.cols.y.values():
    #         n += 1
    #         d += abs(col.heaven - col.norm)
