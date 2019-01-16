import pandas as pd
from pandas.tseries.offsets import YearEnd, YearBegin, BDay, QuarterEnd, QuarterBegin

today = pd.to_datetime('today')

pd.date_range('2011-01-05', '2011-01-09', freq=BDay())

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
weekdays = pd.DatetimeIndex(start=today,end='2019-12-31', freq=us_bd)
print(weekdays.shape[0])


