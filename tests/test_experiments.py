"""Real work counts, growth trends, size caps and narrow-terminal output."""

import random
from time import perf_counter

import pytest
from rich.cells import cell_len

from pydsa.practice import experiments
from pydsa.ui import render
from pydsa.ui.console import console


@pytest.mark.parametrize("experiment", experiments.EXPERIMENTS, ids=lambda e: e.id)
@pytest.mark.parametrize("mode", experiments.MODES)
def test_experiments_are_bounded_and_count_work(experiment, mode):
    start = perf_counter()
    sizes = tuple(sorted({min(n, max(experiment.sizes)) for n in (8, 16, 32)}))
    rows = experiments.measure(experiment, mode, sizes=sizes, rng=random.Random(1))
    assert perf_counter() - start < 2
    assert [row.n for row in rows] == list(sizes)
    assert all(type(row.work) is int and row.work >= 0 and row.milliseconds >= 0 for row in rows)
    assert all(row.ratio == row.work / experiment.expected(row.n) for row in rows)


def test_work_growth_and_ordered_tree_behavior():
    by_id = {experiment.id: experiment for experiment in experiments.EXPERIMENTS}
    sizes = (16, 32, 64, 128)
    def rows(name, mode="sorted"):
        return experiments.measure(by_id[name], mode, sizes=sizes, rng=random.Random(4))
    assert [row.work for row in rows("linear-search")] == list(sizes)
    assert [row.work for row in rows("binary-search")] == [5, 6, 7, 8]
    assert [row.work for row in rows("heap-insert")] == [4, 5, 6, 7]
    assert [row.work for row in rows("hash-probes")] == [n - 1 for n in sizes]
    assert [row.work for row in rows("find-hops")] == [4, 5, 6, 7]
    assert [row.work for row in rows("compressed-find")] == [1] * 4
    ratios = [row.ratio for row in rows("merge-sort", "random")]
    assert max(ratios) / min(ratios) < 1.5
    for mode in ("sorted", "reversed"):
        assert [row.work for row in rows("bst-insert", mode)] == [n - 1 for n in sizes]
        assert all(row.work <= 2 * experiments.LOG(row.n) for row in rows("avl-insert", mode))


def test_size_caps_and_input_modes():
    experiment = experiments.EXPERIMENTS[0]
    for sizes in ((0,), (1,), (10000,), (True,)):
        with pytest.raises(ValueError):
            experiments.measure(experiment, sizes=sizes)
    with pytest.raises(ValueError):
        experiments.measure(experiment, "unknown")
    assert experiments.ordered_input(5, "sorted", random.Random(0)) == list(range(5))
    assert experiments.ordered_input(5, "reversed", random.Random(0)) == list(range(4, -1, -1))
    assert len({experiment.id for experiment in experiments.EXPERIMENTS}) == len(experiments.EXPERIMENTS)


@pytest.mark.parametrize("width", [45, 90])
def test_experiment_tables_fit(width, capsys):
    console.width = width
    for experiment in experiments.EXPERIMENTS:
        sizes = tuple(sorted({min(n, max(experiment.sizes)) for n in (8, 16)}))
        render.experiment(experiment, experiments.measure(experiment, sizes=sizes), "random")
        out = capsys.readouterr().out
        assert all(cell_len(line) <= width for line in out.splitlines())
        if experiment.kind == "bloom-rate":
            assert "Measured" in out and "Formula" in out and "False hits" in out
        else:
            assert "Ratio" in out and "█" in out and "Milliseconds" in out
