import math


class Num:
    def __init__(self, s: str, n: int) -> None:
        self.txt = s if s else " "
        self.at = n if n else 0
        self.n = 0
        self.mu = 0
        self.m2 = 0  # sum of squared distance from mu, used to compute std

        # Arbitrarily small and large numbers, for comparison
        self.hi = -1 * float("inf")
        self.lo = float("inf")

    def add(self, value: float) -> None:
        """Includes a value in the column.

        Args:
            value (float): Value to add
        """
        if value == "?":
            pass
        else:
            self.n += 1
            distance_from_mu = value - self.mu

            # Recalculate mu to include value
            self.mu += distance_from_mu / self.n

            self.m2 += distance_from_mu * (
                value - self.mu
            )  # NOTE: not sure why its not just dist**2

            # Maybe recalculate min and max
            self.lo = min([value, self.lo])
            self.hi = max([value, self.hi])

    def mid(self) -> float:
        return self.mu

    def div(self) -> float:
        """Returns standard deviation.

        Returns:
            float: Std
        """
        if self.n < 2:
            return 0
        else:
            (self.m2 / (self.n - 1)) ** 0.5  # std formula, why self.n - 1?

    def like(self, value: float) -> float:
        """Likelihood of value in distribution assuming normal distribution.

        Args:
            value (float): Value to evaluate

        Returns:
            float: "Likelihood"
        """
        mu = self.mu
        std = self.div() + 1e-30  # add to avoid 0
        distance_from_mu = value - mu

        numerator = math.e ** (-0.5 * (distance_from_mu**2) / (std**2))
        denominator = 2.5 * (math.sqrt(2 * math.pi)) + 1e-30

        return numerator / denominator
