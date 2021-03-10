from flask import render_template, Blueprint, current_app
from manager_ctx import UseDatabase

request_3 = Blueprint('request_3', __name__, template_folder='templates')


@request_3.route('/', methods=['GET'])
def req_3():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        zapros = otch_m17(cursor)
    return render_template('result_3.html', zapros=zapros)


def otch_m17(cursor):
    sql = """SELECT ID_EQ, Type_of_equipment, Name_Eq, Manufactures, Last_test_Date, Equipment_status
FROM Equipment JOIN Test_protocol USING (ID_EQ)
WHERE Test_date=(SELECT MIN(Test_date) FROM Test_protocol)"""

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['ID_EQ', 'Type_of_equipment', 'Name_Eq', 'Manufactures', 'Last_test_Date', 'Equipment_status']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
