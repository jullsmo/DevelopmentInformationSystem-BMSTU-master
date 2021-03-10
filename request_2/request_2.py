from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_2 = Blueprint('request_2', __name__, template_folder='templates')


@request_2.route('/', methods=['GET', 'POST'])
def req_2():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros2 = otch_m17(cursor)
    return render_template('result_2.html', zapros2=zapros2)


def otch_m17(cursor):
    sql = """SELECT Surname, count(ID_TP)
FROM Test_protocol TP JOIN Employee Em USING (ID_EM)
WHERE YEAR(Test_date)=2017 AND MONTH(Test_date)=3 GROUP BY Surname"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema2 = ['Surname', 'count(ID_TP)']
    for blank in result:
        res.append(dict(zip(schema2, blank)))
    return res
