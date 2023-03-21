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
    with open('./yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0
        errorCountUsers = 0
        errorCountFriends = 0
        userId=''

        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            #if (count_line < 10):
                data = json.loads(line)

                # CREATE TABLE Users (
                #     UserId char(22),
                #     Name varchar(30),
                #     YelpingSince varchar(10),
                #     ReviewCount int,
                #     Fans smallint,
                #     AverageStars numeric(3,1),
                #     Funny int,
                #     Useful int,
                #     Cool int,
                #     PRIMARY KEY (UserId)
                # );


                # CREATE TABLE UserFriends (
                #     UserId char(22) NOT NULL,
                #     FriendId char(22) NOT NULL,
                #     PRIMARY KEY (UserId, FriendId),
                #     FOREIGN KEY (UserId) REFERENCES Public.Users(UserId),
                #     FOREIGN KEY (FriendId) REFERENCES Public.Friends(FriendId)
                # );

                userId = cleanStr4SQL(data['user_id'])
                sql_str = "INSERT INTO Users (userid, name, yelpingsince, reviewcount, fans, averagestars, funny, useful, cool) " \
                          "VALUES ('" + userId + "','" \
                          + cleanStr4SQL(data["name"]) + "','" \
                          + cleanStr4SQL(data["yelping_since"]) + "'," \
                          + str(data["review_count"]) + "," \
                          + str(data["fans"]) + "," \
                          + str(data["average_stars"]) + "," \
                          + str(data["funny"]) + "," \
                          + str(data["useful"]) + "," \
                          + str(data["cool"]) + ")"
                try:
                    print(sql_str)
                    cur.execute(sql_str)
                    print("userId:" + str(userId))
                except:
                    print("Insert to User table failed!")
                    errorCountUsers += 1

                conn.commit()

                for friendId in data['friends']:
                    # Insert into category if not in table already.
                    sql_str = "INSERT INTO UserFriends (UserId, FriendId) " \
                              "VALUES('" + userId + "','" + friendId + "')"
                    try:
                        print(sql_str)
                        cur.execute(sql_str)
                    except:
                        print("Insert to UserFriends failed!")
                        errorCountFriends += 1

                    conn.commit()

                line = f.readline()
                count_line += 1
            #else:
                #break

        cur.close()
        conn.close()

    print(count_line)
    print("failures for users:" + str(errorCountUsers))
    print("failures for friends:" + str(errorCountFriends))
    f.close()


insert2ReviewTable()