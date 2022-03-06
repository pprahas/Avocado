import json
from logging import exception
import sqlalchemy as db
from hashlib import sha256

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User is allowed to log into their account.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "User does not exist or the password is incorrect.", "body": {}}

def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            assert content.get( "user_id" ), "User ID not found"
            assert content.get( "user_password" ), "User password not found"
            print(event)


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

    #retrieving from the json file 
    user_id = event.get('user_id')
    user_password = event.get('user_password')

    # print(user_id)
    # print(user_password)

    # connect to db
    engine = db_connection()

    connection = engine.connect()

    user_id_query_count = "SELECT COUNT(user_id) FROM avocado1.user_info where user_id = \'" + user_id + "\';"
    # print (user_id_query_count)
        
    user_id_db_count = connection.execute(user_id_query_count)

    # print(user_id_db_count)

    for row in user_id_db_count:
        user_id_count = row[0]
    
    # print(user_id_count)

    if(user_id_count == 0):
        return MSG_FAIL_TO_CREATE
    

    user_password_query = "SELECT user_password FROM avocado1.user_info where user_id = \'" + user_id + "\';"

    user_password_db_raw = connection.execute(user_password_query)

    for row in user_password_db_raw:
        user_password_db = row[0]
    
    user_password_hashed = sha256(user_password.encode('utf-8')).hexdigest()

    # print("THE USER PASSWORD HASHED IS", user_password_hashed)
    # print ("THE PASSWORD FROM THE DB IS", user_password_db)

    if(user_password_hashed == user_password_db):
        return MSG_SUCCESS
    else:
        return MSG_FAIL_TO_CREATE

    # print(user)
       
    
    try:
        # sql = "INSERT INTO user_info(name, user_id, payment_type, birthday, user_email, user_password) VALUES (%s, %s, %s, %s, %s, %s)" 
        # val = (name, userid, payment, birthday, email, hashed_password)
        # connection.execute(sql,val);
        
        return MSG_SUCCESS

    except Exception as e:
        # print("Email is not unique.")
        return MSG_FAIL_TO_CREATE



if __name__ == "__main__":
    body = {
        "user_id": "44a1279e-9cf0-11ec-bb93-dc1ba10bf9f9",
        "user_password": "Prad#ji"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)