import requests
from io import BytesIO
import dateutil.parser
import time
import pandas as pd, numpy as np, datetime


def round_float(digits):
    def f(x):
        return round(np.float32(x), digits)
    return f

def get_google_data(file_path, symbol, interval, days):
    url = "http://finance.google.com/finance/getprices?q=%s&i=%d&p=%dd&f=d,o,h,l,c,v" % (symbol, interval, days)
    r = requests.get(url)

    with open(file_path, 'w') as out:
        out.write(r.content)

def read_google_data(file_path):
    with open(file_path, 'r') as f:
        # Extract meta-info from preamble
        for index, line in enumerate(f):
            if line.startswith('INTERVAL='):
                interval = int(line[9:])
            if index >= 6:
                break

        # Reset - read_csv does someting different than reading lines
        f.seek(0)

        # Convert the data rows
        data = pd.read_csv(f, skiprows=7, header=None,
                            names=['a', 'Close', 'High', 'Low', 'Open', 'Volume'],
                            converters={'a' : np.str,
                                        'Open' : round_float(4),
                                        'High' : round_float(4),
                                        'Low' : round_float(4),
                                        'Close' : round_float(4),
                                        'Volume' : np.int32 })

        # Create date sequence for index
        for index, row in data.iterrows():
            # Some rows begin with a unix timestamp prefixed by 'a'
            # use that to determine the time
            if row.a[0] == 'a':
                ts = int(row.a.replace('a',''))
                t = datetime.datetime.fromtimestamp(ts)
                data.loc[index, 'Timestamp'] = t

            # The rest of the rows are intervals from the last timestamp
            else:
                offset = interval * int(row.a)
                data.loc[index, 'Timestamp'] = t + pd.to_timedelta(offset, unit='s')

        # Reformat into a pandas dataframe with the date sequence as an index
        data.set_index('Timestamp', inplace=True, drop=True)
        data.drop('a', axis=1, inplace=True)

    return data
