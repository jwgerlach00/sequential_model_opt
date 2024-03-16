from src.Data import Data
from src import utils


class TestDataStats:
    def test(self) -> None:
        data = Data("data/auto93.csv")
        assert (
            utils.output(data.mid_stats())
            == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"
        )
