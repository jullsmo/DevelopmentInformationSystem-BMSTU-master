from flask import render_template, Blueprint, current_app
from manager_ctx import UseDatabase

request_5 = Blueprint('request_5', __name__, template_folder='templates')


@request_5.route('/', methods=['GET'])
def req_5():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros = otch_m17(cursor)
    return render_template('result_5.html', zapros=zapros)


def otch_m17(cursor):
    sql = """SELECT Surname FROM Employee LEFT JOIN Test_protocol USING (ID_EM) WHERE ID_TP is NULL"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['Surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
