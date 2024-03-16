import math


class Sym:
    def __init__(self, s: str, n: int) -> None:
        self.txt = s if s else " "
        self.at = n if n else 0
        self.n = 0
        self.has = {}
        self.mode = None
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
            if self.has[value] > self.mode:
                self.mode = value
                self.most = self.has[value]

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

    def like(self, value: str, prior: float) -> float:
        # implements p(h | e) = (p(e|h) + p(h)) / p(e) NOTE: SOMEHOW???
        # Bayesian statistics
        p_e = self.has[value] if value in self.has else 0

        return (p_e + prior) / self.n
