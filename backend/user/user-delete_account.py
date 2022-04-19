import json
from logging import exception
import sqlalchemy as db
from hashlib import sha256

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "The user's account has successfully been deleted", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "User email does not exist", "body": {}}

def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            assert content.get( "user_email" ), "User email not found"
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
    user_email = event.get('user_email')

    # connect to db
    engine = db_connection()
    connection = engine.connect()

    #checking if the email exists

    user_email_query_count = "SELECT COUNT(user_id) FROM avocado1.user_info where user_email = \'" + user_email + "\';"
    # print (user_id_query_count)
        
    user_email_db_count = connection.execute(user_email_query_count)

    # print(user_id_db_count)

    for row in user_email_db_count:
        user_email_count = row[0]
    
    # print(user_id_count)

    if(user_email_count == 0):
        return MSG_FAIL_TO_CREATE
    
    #checking if password exists

    """ 
    user_password_db_raw = connection.execute(user_password_query)

    for row in user_password_db_raw:
        user_password_db = row[0]
    
    user_password_hashed = sha256(user_password.encode('utf-8')).hexdigest()

    # print("THE USER PASSWORD HASHED IS", user_password_hashed)
    # print ("THE PASSWORD FROM THE DB IS", user_password_db)

    if(user_password_hashed != user_password_db):
        return MSG_FAIL_TO_CREATE

    """

    try:
        # sql = "INSERT INTO user_info(name, user_id, payment_type, birthday, user_email, user_password) VALUES (%s, %s, %s, %s, %s, %s)" 
        # val = (name, userid, payment, birthday, email, hashed_password)
        # connection.execute(sql,val);

        user_account_delete_query = "DELETE FROM avocado1.user_info WHERE user_email = \'" + user_email + "\';"

        connection.execute(user_account_delete_query)
        
        return MSG_SUCCESS

    except Exception as e:
        print("The user account failed to delete.")
        return MSG_FAIL_TO_CREATE

if __name__ == "__main__":
    body = {
        "user_email": "1234@asdf.asdf",
        }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)