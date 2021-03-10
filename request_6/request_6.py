from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_6 = Blueprint('request_6', __name__, template_folder='templates')


@request_6.route('/', methods=['GET', 'POST'])
def req_6():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros = otch_m17(cursor)
    return render_template('result_6.html', zapros=zapros)

def otch_m17(cursor):
    sql = """SELECT * FROM no_test"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['Surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
