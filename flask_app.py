
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    today = pd.to_datetime('today')
    yearEnd = '2019-12-31'
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    remainingBDays = pd.DatetimeIndex(start=today,end=yearEnd, freq=us_bd))
    hours_worked = None
    annual_target = None
    hours_per_day = None
    if request.method == 'POST':
        hours_worked = request.form.get('hours_worked')
        annual_target = request.form.get('annual_target')
        hours_per_day = request.form.get('hours_per_day')
        return render_template('main.html', hours_worked=hours_worked,
             annual_target=annual_target, hours_per_day=hours_per_day)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
