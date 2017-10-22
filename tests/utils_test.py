import pytest

from market_profile.utils import *

class UtilsTest(object):
    def test_midmax_idx(self):
        assert 1 == midmax_idx([1, 4, 2, 3])
        assert 0 == midmax_idx([5140.120268270001, 369.19812357999984])
        assert 0 == midmax_idx([0])
        assert not midmax_idx([])
