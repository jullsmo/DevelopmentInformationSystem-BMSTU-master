import json

from flask import Flask, render_template, request, redirect, Blueprint, current_app, session
from manager_ctx import UseDatabase

main_proc = Blueprint('main_proc', __name__, template_folder='templates')

with open('data_files/access.json', 'r') as f:
    access = json.load(f)


@main_proc.route('/', methods=['GET', 'POST'])
def call_main():
    if session['user_group'] not in access['groups']:
        return render_template('access_error.html')
    if 'send' in request.form and request.form['send'] == 'send': 
        global nameeq, nametest, surnamem, id_pl, year
        nameeq = request.form['nameeq']
        nametest = request.form['nametest']
        surnamem = request.form['surnamem']
        year = request.form['year']

        print(nameeq, nametest, surnamem, year)
        with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
            post(cursor, nameeq, nametest, surnamem, year)

            
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        plan = get(cursor)
        nameeqs = get_nameeqs(cursor)
        nametests = get_nametests(cursor)
        surnamems = get_surnamems(cursor)
    return render_template('enter_main.html', plan_get=plan, nameeqs=nameeqs, nametests=nametests, surnamems=surnamems)


def get_nameeqs(cursor):
    sql = f"select name_eq from equipment;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['name_eq']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def get_nametests(cursor):
    sql = f"select name_test from test_list;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['name_test']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res

def get_surnamems(cursor):
    sql = f"select surname from employee;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res

def get(cursor):
    sql = f"select distinct id_eqs, id_tls, id_ems, date_new from plan" 
       
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['id_eqs', 'id_tls', 'id_ems', 'date_new']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def post(cursor, nameeq, nametest, surnamem, year):
    cursor.execute("""insert into Plan (id_p, id_eqs, id_tls, id_ems, date_new)
        values (Null, (select name_eq from equipment where name_eq='%s'),
        (select name_test from test_list where name_test='%s'),
        (select surname from employee where surname='%s'), '%s'); """  % (nameeq, nametest, surnamem, year))
    


