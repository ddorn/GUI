import pytest
from GUI.colors import *


@pytest.mark.parametrize('color', [
    (200, 200, 201),
    (101, 250, 250),
    (250, 250, 250)
])
def test_w_contrasted(color):
    assert bw_contrasted(color) == BLACK
