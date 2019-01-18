
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, make_response
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay, YearEnd
from decimal import Decimal

app = Flask(__name__)

today = pd.to_datetime('today')
yearEnd = today+YearEnd()
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
holidays = len(USFederalHolidayCalendar().holidays(start=today, end=yearEnd))
remainingBDays = len(pd.DatetimeIndex(start=today,end=yearEnd, freq=us_bd))
workable_days = remainingBDays
days_off = ''

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    blankPage = render_template('main.html', days_off='', holidays='', workable_days='', checked=None)
    hours_worked = request.form.get('hours_worked') or request.cookies.get('hours_worked')
    annual_target = request.form.get('annual_target') or request.cookies.get('annual_target')
    hours_per_day = request.form.get('hours_per_day') or request.cookies.get('hours_per_day')
    include_today = request.form.get('include_today')
    if request.method == 'POST' and hours_worked and annual_target and hours_per_day:
        try:
            hours_worked = float(hours_worked)
            annual_target = int(annual_target)
            hours_per_day = float(hours_per_day)
        except:
            return blankPage
        pyhLeft = annual_target - hours_worked
        daysLeft = (pyhLeft / hours_per_day) - int(bool(include_today))
        days_off = round(Decimal(remainingBDays - daysLeft), 2)
        resp = make_response(render_template('main.html', days_off=days_off,
             holidays=holidays, workable_days=workable_days, hours_worked=hours_worked,
             annual_target=annual_target, hours_per_day=hours_per_day, checked=include_today))
        resp.set_cookie('hours_worked', str(hours_worked))
        resp.set_cookie('annual_target', str(annual_target))
        resp.set_cookie('hours_per_day', str(hours_per_day))
        return resp
    return blankPage

if __name__ == '__main__':
    app.run(debug=True)
