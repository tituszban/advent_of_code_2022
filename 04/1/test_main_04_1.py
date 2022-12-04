from main import find_fully_overlapping_count


def test_main():
    example_input = [
        "2-4,6-8",
        "2-3,4-5",
        "5-7,7-9",
        "2-8,3-7",
        "6-6,4-6",
        "2-6,4-8",
    ]

    assert find_fully_overlapping_count(example_input) == 2
