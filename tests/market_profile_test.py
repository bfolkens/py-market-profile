import pytest

import pandas as pd
from market_profile import MarketProfile, MarketProfileSlice

class MarketProfileTest(object):
    @pytest.fixture(autouse=True)
    def market_profile(self):
        df = pd.read_csv(
            open('tests/fixtures/google.csv', 'r'),
            index_col=['Timestamp'],
            parse_dates=['Timestamp'],
            date_parser=pd.to_datetime
        )
        return MarketProfile(df, row_size=0.05)

    @pytest.fixture(autouse=True)
    def market_profile_slice(self):
        mp = self.market_profile()
        return mp[mp.df.index.min():mp.df.index.max()]

    def test_round_to_row(self, market_profile):
        assert 0.10 == market_profile.round_to_row(0.10)
        assert 0.15 == market_profile.round_to_row(0.11)
        assert 0.15 == market_profile.round_to_row(0.15)

    def test_create_slice(self, market_profile_slice):
        assert isinstance(market_profile_slice, MarketProfileSlice)

    def test_initial_balance(self, market_profile_slice):
        assert [927.74, 935.53] == [round(val, 2) for val in market_profile_slice.initial_balance()]

    def test_open_range(self, market_profile_slice):
        assert [927.74, 927.74] == [round(val, 2) for val in market_profile_slice.open_range()]

    def test_profile_attributes(self, market_profile_slice):
        assert 944.50 == round(market_profile_slice.poc_price, 2)
        assert 961.25 == round(market_profile_slice.balanced_target, 2)
        assert [927.75, 959.30] == [round(val, 2) for val in market_profile_slice.profile_range]
        assert [944.20, 958.95] == [round(val, 2) for val in market_profile_slice.value_area]
