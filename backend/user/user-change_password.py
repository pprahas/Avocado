import json
from logging import exception
import sqlalchemy as db
import re
from hashlib import sha256

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "The user's password has been successfully changed.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "The user's password could not be changed.", "body": {}}

def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT
        
        one_exception = []

        """decorator for input checking"""
        try:
            assert content.get( "user_password" ), "User password not found"
            assert content.get( "new_user_password" ), "New User password not found"
            assert content.get( "confirm_new_user_password" ), "Confirm new User password not found"
            print(event)


        except Exception as e:
            # return data
            return { "status": 422, "statusText": "Account field missing.", "body": str( e ) }
        

         #password input validation
        password = content.get( "new_user_password" )

        if( len(password) < 7):
            one_exception += ["The password needs to be more than 7 characters."]
        res = False

        for ele in password:
            if ele.isupper():
                res = True
                break
            
        if (res == False):
            one_exception += ["The password must contain at least one uppercase character."]
        
        special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:123456789]')
        
        if(special_characters.search(password) == None):
            one_exception += ["The password must contain at least one special character or a number."]
        
        confirm_password = content.get("confirm_new_user_password")

        if(password != confirm_password):
            one_exception += ["The password and the confirm password do not match."]
        
        if(len(one_exception) > 0):
            return { "status": 422, "statusText": "The password requirements have not been met.", "body": one_exception }

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
    user_password = event.get('user_password')
    
    user_password_query = "SELECT user_password FROM avocado1.user_info where user_email = \'" + user_email + "\';"

    user_password_db_raw = connection.execute(user_password_query)

    for row in user_password_db_raw:
        user_password_db = row[0]
    
    user_password_hashed = sha256(user_password.encode('utf-8')).hexdigest()

    # print("THE USER PASSWORD HASHED IS", user_password_hashed)
    # print ("THE PASSWORD FROM THE DB IS", user_password_db)

    if(user_password_hashed != user_password_db):
        return MSG_FAIL_TO_CREATE

    new_user_password = event.get('new_user_password')

    new_user_password_hashed = sha256(new_user_password.encode('utf-8')).hexdigest()

    try:
        print ("hashed_password is " + new_user_password_hashed) 
        sql = "UPDATE user_info SET user_password = \'" + new_user_password_hashed + "\' WHERE user_email = \'" + user_email + "\';"
        #val = (name, userid, payment, birthday, email, hashed_password)
        connection.execute(sql)
        #engine.commit()
        #user_account_delete_query = "DELETE FROM avocado2.user_info WHERE user_email = \'" + user_email + "\';"

#        connection.execute(user_account_delete_query)
        
        return MSG_SUCCESS

    except Exception as e:
        print("The user account failed to delete.")
        return MSG_FAIL_TO_CREATE

if __name__ == "__main__":
    body = {
        "user_email" : "p.prahas@gmail.com",
        "user_password": "Prado-22156",
        "new_user_password" : "Prado-222156",
        "confirm_new_user_password" : "Prado-222156"
        }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)