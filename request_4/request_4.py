from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_4 = Blueprint('request_4', __name__, template_folder='templates')


@request_4.route('/', methods=['GET', 'POST'])
def req_4():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros = otch_m17(cursor)
    return render_template('result_4.html', zapros=zapros)


def otch_m17(cursor):
    sql = """SELECT Surname
FROM Equipment Eq JOIN Test_protocol TP USING (ID_EQ) JOIN Employee Em USING (ID_EM)
WHERE ID_EQ LIKE 15"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['Surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
