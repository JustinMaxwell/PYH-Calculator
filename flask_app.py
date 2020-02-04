from flask import Flask, render_template, request, make_response
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay, YearEnd, YearBegin
from decimal import Decimal

app = Flask(__name__)

today = pd.to_datetime('today')
todays_date = str(today).split(' ')[0]
yearBegin = today-YearBegin()
yearEnd = today+YearEnd()
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
holidays = USFederalHolidayCalendar().holidays(start=today, end=yearEnd, return_name=True)
holidayDates = holidays.index
workable_days_total = Decimal(len(pd.DatetimeIndex(start=yearBegin,end=yearEnd, freq=us_bd)))
worked_days_todate = Decimal(len(pd.DatetimeIndex(start=yearBegin,end=today, freq=us_bd)))
workable_days_remaining = Decimal(len(pd.DatetimeIndex(start=today,end=yearEnd, freq=us_bd)))
days_off = ''

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    hours_worked = request.form.get('hours_worked') or request.cookies.get('hours_worked')
    annual_minimum = request.form.get('annual_minimum') or request.cookies.get('annual_minimum') or 1790
    hours_per_day = request.form.get('hours_per_day') or request.cookies.get('hours_per_day') or 8
    include_today = request.form.get('include_today')
    blankPage = render_template('main.html', days_off='', holidays='', workable_days='', include_today=None, annual_minimum=annual_minimum, hours_per_day=hours_per_day)
    if request.method == 'POST' and hours_worked and annual_minimum and hours_per_day:
        try:
            hours_worked = Decimal(hours_worked)
            annual_minimum = Decimal(annual_minimum)
            hours_per_day = Decimal(hours_per_day)
            checked = include_today
            include_today = bool(include_today)
        except:
            return blankPage
        days_off_total = round(((workable_days_total * 8) - annual_minimum) / 8, 2)
        pyhLeft = annual_minimum - hours_worked
        daysLeft = (pyhLeft / hours_per_day)
        workable_days = workable_days_remaining - Decimal(include_today)
        worked_days = worked_days_todate - Decimal(not include_today)
        days_off = round(workable_days - daysLeft, 2)
        leave_score = round(((days_off/days_off_total) - ((workable_days)/workable_days_total)) * 100, 2)
        pyh_score = round(((hours_worked/annual_minimum) - ((worked_days + include_today)/workable_days_total)) * 100, 2)
        resp = make_response(render_template('main.html', 
            days_off=f"{days_off} of {days_off_total}", pyh_score=f"{leave_score} / {pyh_score}", today=todays_date,
            holidays=len(holidays), workable_days=f"{workable_days} of {workable_days_total}", hours_worked=hours_worked, 
            annual_minimum=annual_minimum, hours_per_day=hours_per_day, include_today=checked))
        resp.set_cookie('hours_worked', str(hours_worked))
        resp.set_cookie('annual_minimum', str(annual_minimum))
        resp.set_cookie('hours_per_day', str(hours_per_day))
        return resp
    return blankPage

if __name__ == '__main__':
    app.run(debug=True)
