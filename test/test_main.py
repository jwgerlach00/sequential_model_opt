from src.Data import Data
from src.Row import Row
from src import utils
from src.config import config


class TestData:
    def test_stats(self) -> None:
        data = Data("data/auto93.csv")
        assert (
            utils.output(data.mid_stats())
            == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"
        )


class TestNaiveBayes:
    def test_diabetes(self) -> None:
        outputs = {"acc": 0, "tries": 0, "datas": {}, "n": 0}
        Data(
            "data/diabetes.csv",
            func=lambda data, row: learn_callback(data, row, outputs),
        )

        accuracy = outputs["acc"] / outputs["tries"]
        assert accuracy > 0.70

    def test_soybean_vary_k_and_m(self) -> None:
        original_k = config.k
        original_m = config.m

        accuracies = {}
        for k in range(4):
            for m in range(1, 4):
                config.k = k
                config.m = m

                outputs = {"acc": 0, "tries": 0, "datas": {}, "n": 0}
                Data(
                    "data/soybean.csv",
                    func=lambda data, row: learn_callback(data, row, outputs),
                )
                accuracies[(k, m)] = outputs["acc"] / outputs["tries"]

        # Reset config values
        config.k = original_k
        config.m = original_m

        max_accuracy = 0
        max_key = None
        for key, value in accuracies.items():
            if value > max_accuracy:
                max_accuracy = value
                max_key = key

        assert max_accuracy > 0.84
        assert max_key == (2, 1)  # optimal k and m values


def learn_callback(data: "Data", row: "Row", outputs: dict) -> None:
    outputs["n"] += 1

    klass_index = data.cols.klass.at
    klass = row.cells[klass_index]

    if outputs["n"] > 10:
        outputs["tries"] += 1
        outputs["acc"] += (
            1 if row.likes(outputs["datas"], outputs["n"])[0] == klass else 0
        )

    if klass not in outputs["datas"]:
        outputs["datas"][klass] = Data(data.cols.names)
    outputs["datas"][klass].add(row, None)
