import pytest

import pandas as pd
from market_profile import MarketProfile, MarketProfileSlice

class MarketProfileTest(object):
    @pytest.fixture(autouse=True)
    def market_profile(self):
        df = pd.read_csv(
            'tests/fixtures/google.csv',
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

    def test_as_dict(self, market_profile_slice):
        assert {'or_low': 927.74, 'or_high': 927.74, 'ib_low': 927.74, 'ib_high': 935.53, 'poc': 944.50, 'low': 927.75, 'high': 959.30, 'val': 944.20, 'vah': 958.95, 'bt': 961.25} == market_profile_slice.as_dict()
