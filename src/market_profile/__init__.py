import pandas as pd
import numpy as np
import math
from scipy.signal import argrelextrema
from .utils import midmax_idx


class MarketProfile(object):
    def __init__(self, df, **kwargs):
        self.df = df
        self.tick_size = kwargs.pop('tick_size', 0.05)
        self.prices_per_row = kwargs.pop('prices_per_row', 1)
        self.row_size = kwargs.pop('row_size', self.tick_size * self.prices_per_row)
        self.open_range_delta = kwargs.pop('open_range_size', pd.to_timedelta('10 minutes'))
        self.initial_balance_delta = kwargs.pop('initial_balance_delta', pd.to_timedelta('1 hour'))
        self.value_area_pct = kwargs.pop('value_area_pct', 0.70)
        self.mode = kwargs.pop('mode', 'vol') # or tpo

    def __getitem__(self, index):
        if isinstance(index, slice):
            return MarketProfileSlice(self, slice(index.start, index.stop))
        else:
            raise TypeError("index must be int or slice")

    def round_to_row(self, x):
        if np.isnan(np.float64(x)):
            return x

        roundoff = 1 / float(self.row_size)
        return math.ceil(float(x) * roundoff) / roundoff


class MarketProfileSlice(object):
    def __init__(self, market_profile, _slice):
        self.mp = market_profile
        self.ds = self.mp.df[_slice]
        self.build_profile()

    def open_range(self):
        end = self.ds.iloc[0].name + self.mp.open_range_delta
        ds = self.ds.loc[:end]
        return np.min(ds['Low']), np.max(ds['High'])

    def initial_balance(self):
        end = self.ds.iloc[0].name + self.mp.initial_balance_delta
        ds = self.ds.loc[:end]
        return np.min(ds['Low']), np.max(ds['High'])

    def calculate_value_area(self):
        target_vol = self.total_volume * self.mp.value_area_pct
        trial_vol = self.poc_volume

        min_idx = self.poc_idx
        max_idx = self.poc_idx

        while trial_vol <= target_vol:
            last_min = min_idx
            last_max = max_idx

            next_min_idx = np.clip(min_idx - 1, 0, len(self.profile) - 1)
            next_max_idx = np.clip(max_idx + 1, 0, len(self.profile) - 1)

            low_volume = self.profile.iloc[next_min_idx] if next_min_idx != last_min else None
            high_volume = self.profile.iloc[next_max_idx] if next_max_idx != last_max else None

            if not high_volume or (low_volume and low_volume > high_volume):
                trial_vol += low_volume
                min_idx = next_min_idx
            elif not low_volume or (high_volume and low_volume <= high_volume):
                trial_vol += high_volume
                max_idx = next_max_idx
            else:
                break

        return self.profile.index[min_idx], self.profile.index[max_idx]

    def calculate_balanced_target(self):
        area_above_poc = self.profile.index.max() - self.poc_price
        area_below_poc = self.poc_price - self.profile.index.min()

        if area_above_poc >= area_below_poc:
            bt = self.poc_price - area_above_poc
        else:
            bt = self.poc_price + area_below_poc

        return bt

    def find_extrema(self, sign):
        (extrema_idx,) = argrelextrema(self.profile.values, sign)
        return self.profile.iloc[extrema_idx.tolist()]

    # Calculate the market profile distribution (histogram)
    # http://eminimind.com/the-ultimate-guide-to-market-profile/
    def build_profile(self):
        rounded_set = self.ds['Close'].apply(lambda x: self.mp.round_to_row(x))

        if self.mp.mode == 'tpo':
            self.profile = self.ds.groupby(rounded_set)['Close'].count()
        elif self.mp.mode == 'vol':
            self.profile = self.ds.groupby(rounded_set)['Volume'].sum()
        else:
            raise ValueError("Unrecognized mode: %s" % self.mp.mode)

        self.total_volume = self.profile.sum()
        self.profile_range = self.profile.index.min(), self.profile.index.max()
        self.poc_idx = midmax_idx(self.profile.values.tolist())
        if self.poc_idx is not None:
            self.poc_volume = self.profile.iloc[self.poc_idx]
            self.poc_price = self.profile.index[self.poc_idx]
            self.value_area = self.calculate_value_area()
            self.balanced_target = self.calculate_balanced_target()
        else:
            self.poc_volume = None
            self.poc_price = None
            self.value_area = [None, None]
            self.balanced_target = None

        self.low_value_nodes = self.find_extrema(np.less)
        self.high_value_nodes = self.find_extrema(np.greater)

    def as_dict(self):
        ib_low, ib_high = self.initial_balance()
        or_low, or_high = self.open_range()
        profile_low, profile_high = self.profile_range
        val, vah = self.value_area

        return({
            'or_low': or_low,
            'or_high': or_high,
            'ib_low': ib_low,
            'ib_high': ib_high,
            'poc': self.poc_price,
            'low': profile_low,
            'high': profile_high,
            'val': val,
            'vah': vah,
            'bt': self.balanced_target,
            'lvn': self.low_value_nodes,
            'hvn': self.high_value_nodes
        })
