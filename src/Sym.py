import math
from typing import Any
from src.config import config


class Sym:
    def __init__(self, s: str, n: int) -> None:
        self.txt = s if s else " "
        self.at = n if n else 0
        self.n = 0
        self.has = {}
        self.mode = -1 * float("inf")
        self.most = 0

    def add(self, value: str) -> None:
        """Includes a value in the column.

        Args:
            value (str): Value to add
        """
        if value == "?":
            pass
        else:
            self.n += 1

            # Add entry to has
            if value in self.has:
                self.has[value] += 1
            else:
                self.has[value] = 1

            # Maybe recalculate mode, most
            if self.has[value] > self.most:
                self.mode = value
                self.most = self.has[value]

    def mid(self) -> int:
        """Returns mode.

        Returns:
            float: Mode
        """
        return self.mode

    def div(self) -> float:
        """Returns entropy.

        Returns:
            float: Entropy (positive value)
        """
        entropy = 0
        for count in self.has.values:
            p = count / self.n
            entropy -= p * math.log2(p)
        return entropy

    def like(self, value: Any, prior: float) -> float:
        # implements p(h | e) = (p(e|h) + p(h)) / p(e)
        # Bayesian statistics
        p_e_given_h = self.has[value] if value in self.has else 0  # p(e|h)

        # Formula below: p(e|h) + p(h) normalized (divide by self.n)
        # since we are comparing classes and normalizing we do not need p(e) because it
        # will cancel out anyways
        return (p_e_given_h + config.m * prior) / (self.n + config.m)
