from flask import Flask, render_template, request, make_response
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay, YearEnd, YearBegin
from decimal import Decimal
import requests

app = Flask(__name__)

today = pd.to_datetime('today')
todays_date = str(today).split(' ')[0][5:]
yearBegin = today-YearBegin()
yearEnd = today+YearEnd()
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
holidays = USFederalHolidayCalendar().holidays(start=today, end=yearEnd, return_name=True)
holidayDates = holidays.index
workable_days_total = Decimal(len(pd.DatetimeIndex(start=yearBegin,end=yearEnd, freq=us_bd)))
worked_days_todate = Decimal(len(pd.DatetimeIndex(start=yearBegin,end=today, freq=us_bd)))
progress = round((worked_days_todate/workable_days_total) * 100, 0)
workable_days_remaining = Decimal(len(pd.DatetimeIndex(start=today,end=yearEnd, freq=us_bd)))
days_off = ''

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    hours_worked = request.form.get('hours_worked') or request.cookies.get('hours_worked')
    annual_minimum = request.form.get('annual_minimum') or request.cookies.get('annual_minimum') or 1790
    hours_per_day = request.form.get('hours_per_day') or request.cookies.get('hours_per_day') or 8
    include_today = request.form.get('include_today')
    blankPage = render_template('main.html', days_off='', workable_days='', pyh_score='', today=f"{todays_date} ({progress}%)", include_today=None, annual_minimum=annual_minimum, hours_per_day=hours_per_day)
    if request.method == 'POST' and hours_worked and annual_minimum and hours_per_day:
        try:
            # unanet_time = get_report(user, passwd)
            hours_worked = Decimal(hours_worked)
            annual_minimum = Decimal(annual_minimum)
            hours_per_day = Decimal(hours_per_day)
            checked = include_today
            include_today = bool(include_today)
        except:
            return blankPage
        days_off_total = round(((workable_days_total * 8) - annual_minimum) / 8, 2)
        hours_left = annual_minimum - hours_worked
        days_left = (hours_left / hours_per_day)
        hours_worked_percent = hours_worked/annual_minimum
        workable_days = workable_days_remaining - Decimal(include_today)
        workable_days_percent = workable_days/workable_days_total
        worked_days = worked_days_todate - Decimal(not include_today)
        worked_days_percent = worked_days/workable_days_total
        days_off_remaining = round(workable_days - days_left, 2)
        days_off_remaining_percent = (days_off_remaining/days_off_total)
        leave_score = round((days_off_remaining_percent - workable_days_percent) * 100, 2)
        pyh_score = round((hours_worked_percent - worked_days_percent) * 100, 2)
        resp = make_response(render_template('main.html', 
            days_off=f"{days_off_remaining}", pyh_score=f"{leave_score} / {pyh_score}", 
            today=f"{todays_date} ({progress}%)",
            workable_days=f"{workable_days}", hours_worked=hours_worked, 
            annual_minimum=annual_minimum, hours_per_day=hours_per_day, include_today=checked))
        resp.set_cookie('hours_worked', str(hours_worked))
        resp.set_cookie('annual_minimum', str(annual_minimum))
        resp.set_cookie('hours_per_day', str(hours_per_day))
        return resp
    return blankPage

def get_report(login,passwd):
    from bs4 import BeautifulSoup
    import base64

    def b64(text):
        return base64.b64encode(text.encode()).decode()

    login_url = "https://eurekastrategic.unanet.biz/eurekastrategic/action/login/validate"
    path_info = b64("/eurekastrategic/action/reports/user/summary/time/report")
    query_string = b64(f"loadValues=true&targetPath=/reports/user/summary/time/report&managerPath=/reports/user/summary/time/search&criteriaClass=com.unanet.page.reports.search.UserTimeSummarySearch$UserTimeSummaryCriteria&project_mod=false&projectClass=com.unanet.page.criteria.UserProjectComboMenu&dateRange=c_yr&adjustment=ENTERED&pendingAdjustment=true") 

    data = {'username': login,
    'password': passwd,
    'button_ok': True,
    'pathInfo': path_info,
    "queryString": query_string}

    session = requests.Session()
    resp = session.post(login_url, data=data)

    # HTML Response to dictionary of results
    soup = BeautifulSoup(resp.text, 'html.parser')
    tds = [row.findAll('td') for row in soup.table.findAll('tr')]
    headers = tds[0]
    results  = {"data":[]}
    for td in tds[1:]:
        if len(td) == 3:
            results['data'].append({headers[0].string:td[0].string, headers[1].string:td[1].string, headers[2].string:td[2].string})
        elif len(td) == 2:
            results[td[0].string] = td[1].string
        else:
            raise Exception("Unexpected results")

    pyh_hours = 0
    for entry in results['data']: 
        if entry['Project'] != 'TIME_OFF': 
            pyh_hours += float(entry['Hours'])
    return pyh_hours

if __name__ == '__main__':
    app.run(debug=True)
