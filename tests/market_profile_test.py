import pytest

import pandas as pd
from market_profile import MarketProfile

class MarketProfileTest(object):
    @pytest.fixture(autouse=True)
    def market_profile(self):
        df = pd.read_csv('tests/fixtures/google.csv', 'r')
        return MarketProfile(df, row_size=0.1)

    def test_round_to_row(self, market_profile):
        assert 0.10 == market_profile.round_to_row(0.10)
        assert 0.20 == market_profile.round_to_row(0.11)
        assert 0.20 == market_profile.round_to_row(0.15)
