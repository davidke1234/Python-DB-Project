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

def insert2BusinessTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        busErrorCount=0
        catErrorCount=0
        selCatErrorCount=0
        attErrorCount=0
        selAttErrorCount = 0
        busCatErrorCount=0
        busAttErrorCount = 0
        categoryId=0
        businessId=''
        attributeId=0

        #connect to yelpdb database on postgres server using psycopg2

        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            businessId = cleanStr4SQL(data['business_id'])
            sql_str = "INSERT INTO Business (BusinessId, Name, Address,State,City,PostalCode,Stars,ReviewCount) " \
                      "VALUES ('" + businessId + "','" + cleanStr4SQL(data["name"]) \
                      + "','" + cleanStr4SQL(data["address"]) \
                      + "','" + cleanStr4SQL(data["state"]) \
                      + "','" + cleanStr4SQL(data["city"]) \
                      + "','" + cleanStr4SQL(data["postal_code"]) \
                      + "'," + str(data["stars"]) \
                      + "," + str(data["review_count"]) + ")"
            try:
                print(sql_str)
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
                busErrorCount += 1

            conn.commit()

            # *** Process Category Data ***
            for category in data['categories']:
                # Insert into category if not in table already.
                sql_str = "INSERT INTO category (CategoryName) " \
                    " SELECT '" + cleanStr4SQL(category) + "'" \
                    " WHERE NOT EXISTS (SELECT categoryId FROM Category WHERE CategoryName = '" \
                          + cleanStr4SQL(category) + "')"

                try:
                    print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to Category failed!")
                    catErrorCount += 1

                conn.commit()

                sql_str = "SELECT categoryId FROM Category WHERE CategoryName = '" + cleanStr4SQL(category) + "'"

                try:
                    print(sql_str)
                    cur.execute(sql_str)
                    results = cur.fetchone()
                    categoryId = results[0]
                    print("catId:" + str(categoryId))
                except:
                    print("select from Category failed!")
                    selCatErrorCount += 1

                conn.commit()

                #Insert into businessCategory
                sql_str = "INSERT INTO businessCategory (businessId, categoryId) " \
                          " VALUES('" + businessId + "'," + str(categoryId) + ")"
                try:
                    print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to businessCategory failed!")
                    busCatErrorCount += 1

                conn.commit()

            # Process Attributes
            for (attributeName, attributeValue) in getAttributes(data['attributes']):
                # Insert into attributes if not in table already.
                sql_str = "INSERT INTO Attribute (AttributeName) " \
                          " SELECT '" + cleanStr4SQL(attributeName) + "'" \
                          " WHERE NOT EXISTS (SELECT AttributeId FROM Attribute WHERE attributeName = '" \
                          + cleanStr4SQL(attributeName) + "')"

                try:
                    print(sql_str)
                    cur.execute(sql_str)
                    results = cur.fetchone()
                    attributeId = results[0]
                    print("attrId:" + str(attributeId))
                except:
                    print("Insert to Attribute failed!")
                    attErrorCount += 1

                conn.commit()

                sql_str = "SELECT attributeId FROM Attribute WHERE attributeName = '" + cleanStr4SQL(attributeName) + "'"

                try:
                    print(sql_str)
                    cur.execute(sql_str)
                    results = cur.fetchone()
                    attributeId = results[0]
                    print("attrId:" + str(attributeId))
                    print("attrValue:" + str(attributeValue))
                except:
                    print("select from attribute failed!")
                    selAttErrorCount += 1

                conn.commit()

                # process business attributes
                sql_str = "INSERT INTO businessAttribute (businessId, AttributeId, AttributeValue)" \
                          " VALUES('" + businessId + "'," + str(attributeId) + ",'" + str(attributeValue) + "')"
                try:
                    print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to businessAttribute failed!")
                    busAttErrorCount += 1

                conn.commit()

                # optionally you might write the INSERT statement to a file.
                # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    print("failures for bus:" + str(busErrorCount))

    print("failures for bus:" + str(catErrorCount))
    print("failures for bus:" + str(selCatErrorCount))
    print("failures for bus:" + str(busCatErrorCount))

    print("failures for bus:" + str(attErrorCount))
    print("failures for bus:" + str(selAttErrorCount))
    print("failures for bus:" + str(busAttErrorCount))

    f.close()


insert2BusinessTable()