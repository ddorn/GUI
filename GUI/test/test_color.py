import pytest

from GUI.colors import bw_contrasted
from GUI.locals import BLACK


@pytest.mark.parametrize('color', [
    (200, 200, 201),
    (101, 250, 250),
    (250, 250, 250)
])
def test_w_contrasted(color):
    assert bw_contrasted(color) == BLACK
