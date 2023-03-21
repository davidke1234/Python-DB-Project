import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def insert2Table():
    #reading the JSON file
    with open('./yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0
        errorCount = 0

        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')

        cur = conn.cursor()

        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek, time) in data['time'].items():
                for (hour, count) in time.items():
                    checkin_str = "'" + business_id + "'," \
                                  "'" + dayofweek + "'," + \
                                  "'" + hour + "'," + \
                                  str(count)

                    sql_str = "insert into BusinessCheckin (BusinessId, CheckinWeekDay, CheckinHour, CheckinCount) VALUES " \
                              + "(" + checkin_str + ")"
                    try:
                        print(sql_str)
                        cur.execute(sql_str)
                    except:
                        print("Insert to BusinessCheckin table failed!")
                        errorCount += 1

                    conn.commit()
                    count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    print("bus checkin failures:" + str(errorCount))
    f.close()


insert2Table()