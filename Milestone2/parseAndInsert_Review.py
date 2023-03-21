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

def insert2ReviewTable():
    #reading the JSON file
    with open('./yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0
        errorCountReview = 0
        errorCountBusinessReview = 0

        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            #if (count_line < 10):
                data = json.loads(line)

                sql_str = "INSERT INTO Review (ReviewId, ReviewDate, Text, Stars, Useful, funny, cool) " \
                          "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" \
                          + cleanStr4SQL(data["date"]) + "','" \
                          + cleanStr4SQL(data["text"]) + "'," \
                          + str(data["stars"]) + "," \
                          + str(data["useful"]) + "," \
                          + str(data["funny"]) + "," \
                          + str(data["cool"]) + ")"
                try:
                    print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to Review table failed!")
                    errorCountReview += 1

                conn.commit()

                sql_str = "INSERT INTO BusinessReview (ReviewId, UserId, BusinessId) " \
                          "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" \
                          + cleanStr4SQL(data["user_id"]) + "','" \
                          + cleanStr4SQL(data["business_id"]) + "')"
                try:
                    print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to BusinessReview table failed!")
                    errorCountBusinessReview += 1

                conn.commit()

                line = f.readline()
                count_line += 1
            #else:
                #break

        cur.close()
        conn.close()

    print(count_line)
    print("failures for review:" + str(errorCountReview))
    print("failures for business review:" + str(errorCountBusinessReview))
    f.close()


insert2ReviewTable()