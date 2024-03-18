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


class TestGate:
    @staticmethod
    def _format_dict(d: dict) -> str:
        s = ""
        for i, row_data in d.items():
            s += f"row {i + 1}: {row_data}\n"
        return s

    @staticmethod
    def _get_top_rows_ys(data: "Data", n: int) -> dict:
        y_column_indices = list(data.cols.y.keys())
        top_rows = data.slice_rows(0, n)

        top_n_rows = {
            i: [row.cells[y] for y in y_column_indices] for i, row in top_rows.items()
        }
        return top_n_rows

    # @staticmethod
    # def _get_bottom_rows(data: "Data", n: int) -> dict:
    #     y_column_indices = list(data.cols.y.keys())
    #     bottom_rows = data.slice_rows(n)

    #     bottom_n_rows = {
    #         i: [row.cells[y] for y in y_column_indices]
    #         for i, row in bottom_rows.items()
    #     }
    #     return bottom_n_rows

    def test_auto(self) -> None:
        data = Data("data/auto93.csv")
        data.shuffle()

        print("top6 ---")
        print(self._format_dict(self._get_top_rows_ys(data, 6)))

        print("top50 ---")
        print(self._format_dict(self._get_top_rows_ys(data, 50)))

        # This is the baseline, it involves looking at every y
        # This will be the absolute best example (or one of them if equal)
        data.rows = utils.sort_by_d2h(data.rows, data)
        d2h1 = data.rows[0].d2h(data)

        # Do it again to prove it is the same
        data.shuffle()
        data.rows = utils.sort_by_d2h(data.rows, data)
        d2h2 = data.rows[0].d2h(data)
        assert d2h1 == d2h2

        print("most (sorted by d2h) ---")
        print(self._format_dict(self._get_top_rows_ys(data, 1)))

        stats, bests = data.gate(budget0=4, budget=10)

        bests_data = Data(data.cols.names)
        d2hs = []
        for row in bests.values():
            bests_data.add(row, None)
            d2hs.append(row.d2h(data))

        # Show that they get better over time
        print("\nbests output ---")  # \n because of prints in data.gate
        print(self._format_dict(self._get_top_rows_ys(bests_data, len(bests))))
        for i in range(1, len(d2hs)):  # ensure monotonically non-increasing
            assert d2hs[i] <= d2hs[i - 1]

        stats_data = Data(data.cols.names)
        for row in stats.values():
            stats_data.add(row, None)

        print("stats output ---")
        print(self._format_dict(self._get_top_rows_ys(stats_data, len(stats))))


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
