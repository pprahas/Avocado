from base64 import encode
import json
import sqlalchemy as db
import datetime
from hashlib import sha256
from datetime import datetime
import random


MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}

def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            # assert content.get( "firstName" ), "First Name not found"
            # assert content.get( "lastName" ), "Last Name not found"
            # assert content.get( "email" ), "Email not found."
            # assert content.get( "birthday" ), "Birthday not found."
            # assert content.get( "password" ), "Password not found."
            pass

        except Exception as e:
            # return data
            return { "status": 422, "statusText": "Account field missing.", "body": str( e ) }

        # return function
        return func( content, context )

    # return
    return inner

def db_connection():
    username = "admin"
    password = "avocado123"
    server = "avocado-348.cgooazgc1htx.us-east-1.rds.amazonaws.com"
    database = "avocado1"

    db_url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
    engine = db.create_engine(db_url, echo=False)
    engine.connect()

    return engine

@input_checking   
def lambda_handler(event, context):
    # TODO implement
    fname = event.get('name')
    user_id = int(event.get('user_id'))
    payment_type = event.get('payment_type')
    birthday = event.get('birthday')
    user_email = event.get('user_email')
    user_password = event.get('user_password')

    # running the sha256 hashing algorithm
    h = sha256()
    h.update(b'user_password')
    # user_password = h.hexdigest()
      
    print(fname)
    # print(user_id)
    # print(payment_type)
    # print(birthday)
    # print(user_email)
    # print(user_password)

    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    birthday = birthday.strftime('%Y-%m-%d %H:%M:%S')

    # version 1----------------------------------------------------------------------------------------------------------
    # # take note that string and date need '', integer doesn't.

    # sql = """INSERT INTO user_info (name, user_id, payment_type, birthday, user_email, user_password)
    #                 VALUES ('{}', {}, '{}', '{}', '{}', '{}');
    #     """.format(name, user_id, payment_type, 
    #                 birthday, user_email, user_password)

    # # # connect to db
    # engine = db_connection()

    # connection = engine.connect()

    # connection.execute(sql)


    # version 2----------------------------------------------------------------------------------------------------------
    # sql = "INSERT INTO user_info(name, user_id, payment_type, birthday, user_email, user_password) VALUES (%s, %s, %s, %s, %s, %s)" 
    # val = (name, random.randint(1000,9999999), payment_type, birthday, user_email, user_password)

    # connect to db
    engine = db_connection()

    connection = engine.connect()

    # connection.execute(sql,val)

    rows = connection.execute(
       """
       create table user_info(
       name VARCHAR(45),
       user_id VARCHAR(50),
       payment_type VARCHAR(45),
       birthday DATE,
       user_email VARCHAR(45) UNIQUE,
       user_password VARCHAR(64),
       PRIMARY KEY( user_id )
       );
       """)

    # connection.execute(
    #     """
    #     DROP TABLE user_info;
    #     """
    # )


    try:

        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE



if __name__ == "__main__":
    body = {
        "name": "Bulldog2123",
        "user_id": "435345",
        "payment_type": "Cash13",
        "birthday": "2001-11-05",
        "user_email": "bulldog@gmail.commm",
        "user_password": "pwefwf@2ht3"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)