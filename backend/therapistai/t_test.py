from therapistai import t
import pytest

# pytest t_test.py -v
# Funtion based
@pytest.mark.parametrize(
    ('input_n', 'expected'),
    (
        (5, 25),
        (3., 9.),
    )
)
def test_square(input_n, expected):
    assert t.square(input_n,) == expected

# def test_square():
#     assert t.square(5) == 25

# def test_square_float():
#     assert t.square(3.) == 9.

# Class based
class TestSquare:
    def test_sqare(self):
        assert t.square(3) == 9
