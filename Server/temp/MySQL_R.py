import pymysql

db = pymysql.connect(host='',
                     port=8883,
                     user='',
                     password='',
                     db='',
                     charset="utf8")

cursor = db.cursor()

sql = "SELECT * FROM shebei_in"

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        number = row[0]
        id_in = row[1]
        name_in = row[2]
        status = row[3]
        print ("N=%s I=%s N=%s S=%s" % (number, id_in, name_in, status))

except:
    print ("Error!")

db.close()