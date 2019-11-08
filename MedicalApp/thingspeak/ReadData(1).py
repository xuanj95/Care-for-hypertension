import urllib.request
import json
import time
import ssl
import pymysql

ssl._create_default_https_context = ssl._create_unverified_context

# lamdba 表达式，将None转换成0
f = lambda x : int(x)  if(x!=None) else 0

while True:
    TS = urllib.request.urlopen("https://api.thingspeak.com/channels/890226/feeds.json?results=4")
    conn = pymysql.connect(host="localhost", user="root", password="xuyifudick123", database="medical", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    response = TS.read().decode('UTF-8')
    data = json.loads(response)         #读取数据
    array = []                        #创建数组来接收所有数据
    b = data.setdefault('feeds', 0)     #读取数据的feed部分
    TimeNow = time.strftime("%Y-%m-%d", time.localtime())
    # print(b)
    for i in range(len(b)):
        array.append((f(b[i]['field1']),f(b[i]['field4']),f(b[i]['field3']),f(b[i]['field2']),TimeNow))  #将读取的数据填入array中
    for i in range(len(array)):
        if array[i] != []:
            print(array[i])             #输出需要的数组
            data = [19,]+list(array[i])
            sql = "INSERT INTO medical_indicators (userId_id,heartRate,systolicBloodPressure,diastolicBloodPressure,bloodOxygenation,CreateDate) VALUES (%s,%s,%s,%s,%s,%s);"
            try:
                # cursor.execute(sql, data)
                conn.commit()
                print("add successfully")
            except Exception as e:
                print(str(e))
            #     # conn.rollback()

    cursor.close()
    conn.close()
    time.sleep(5)
    TS.close()
