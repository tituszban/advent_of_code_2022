from main import score_round, evaluate


def test_rps():
    assert score_round("A", "X") == 3 + 1
    assert score_round("A", "Y") == 6 + 2
    assert score_round("A", "Z") == 0 + 3
    assert score_round("B", "X") == 0 + 1
    assert score_round("B", "Y") == 3 + 2
    assert score_round("B", "Z") == 6 + 3
    assert score_round("C", "X") == 6 + 1
    assert score_round("C", "Y") == 0 + 2
    assert score_round("C", "Z") == 3 + 3


def test_example():
    example_input = [
        ["A", "Y"],
        ["B", "X"],
        ["C", "Z"]
    ]
    assert evaluate(example_input) == 15
