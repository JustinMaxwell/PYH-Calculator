
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay, YearEnd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    today = pd.to_datetime('today')
    yearEnd = today+YearEnd()
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    holidays = len(USFederalHolidayCalendar().holidays(start=today, end=yearEnd))
    remainingBDays = len(pd.DatetimeIndex(start=today,end=yearEnd, freq=us_bd))
    workable_days = remainingBDays
    days_off = None
    if request.method == 'POST':
        hours_worked = request.form.get('hours_worked')
        annual_target = request.form.get('annual_target')
        hours_per_day = request.form.get('hours_per_day')
        return render_template('main.html', days_off=days_off,
             holidays=holidays, workable_days=workable_days)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
