import json

from flask import render_template, request, Blueprint, current_app, session
from manager_ctx import UseDatabase

proc = Blueprint('proc', __name__, template_folder='templates')


with open('data_files/access.json', 'r') as f:
    access = json.load(f)


@proc.route('/', methods=['GET', 'POST'])
def call():
    if session['user_group'] not in access['groups']:
        return render_template('access_error.html')
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']

        print(year, month)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                zapros = otch(cursor, year, month)
            return render_template('result_proc.html', zapros=zapros)
        else:
            return render_template('enter_proc.html')
    else:
        return render_template('enter_proc.html')


def otch(cursor, year, month):
    args = (year, month,)
    cursor.execute(f"truncate table otchet;")
    result_procedure = cursor.callproc('otchet', args)
    sql = """select O_ID, O_Year, O_Month, Surname, Kol_test from otchet"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['O_ID', 'O_Year', 'O_Month', 'Surname', 'Kol_test']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
