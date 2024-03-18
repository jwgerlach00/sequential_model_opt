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

        self.heaven = 0 if "-" in s else 1

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
            return (self.m2 / (self.n - 1)) ** 0.5  # std formula

    def like(self, value: float, _) -> float:
        """Likelihood of value in distribution assuming normal distribution.

        Args:
            value (float): Value to evaluate

        Returns:
            float: "Likelihood"
        """
        mu = self.mid()
        std = self.div() + 1e-30  # add to avoid 0
        distance_from_mu = value - mu

        numerator = math.e ** (-0.5 * (distance_from_mu**2) / (std**2))
        denominator = std * (math.sqrt(2 * math.pi)) + 1e-30

        return numerator / denominator

    def norm(self, value: float) -> float:
        """Normalize a value with respect to the column distribution. Uses min max
        normalization.

        Args:
            value (float): Value to normalize

        Returns:
            float: Normalized value
        """
        if value == "?":
            return value
        return (value - self.lo) / (self.hi - self.lo + 1e-30)  # avoid divide by 0
