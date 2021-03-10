from flask import render_template, Blueprint, current_app
from manager_ctx import UseDatabase

request_1 = Blueprint('request_1', __name__, template_folder='templates')


@request_1.route('/', methods=['GET'])
def req_1():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros1 = otch_m17(cursor)
    return render_template('result_1.html', zapros1=zapros1)


def otch_m17(cursor):
    sql = """SELECT ID_EQ, Name_Eq, Surname, Results_status
FROM Equipment Eq JOIN Test_protocol TP USING (ID_EQ) JOIN Employee Em USING (ID_EM)
WHERE YEAR(Test_date)=2017 AND MONTH(Test_date)=3 GROUP BY ID_EQ, Name_Eq"""
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = [ 'ID_EQ', 'Name_Eq', 'Surname', 'Results_status']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
