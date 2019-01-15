
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'POST':
      hours_worked = request.form.get('hours_worked')
      annual_target = request.form.get('annual_target')
      hours_per_day = request.form.get('hours_per_day')
      return render_template('main.html', hours_worked=hours_worked, annual_target=annual_target, hours_per_day=hours_per_day)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
