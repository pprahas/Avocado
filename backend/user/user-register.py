import json
import sqlalchemy as db
import datetime
from datetime import datetime
import re
from hashlib import sha256
import uuid

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Input is invalid.", "body": {}}


def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            assert content.get( "name" ), "Name not found"
            assert content.get( "payment" ), "Payment information not found"
            assert content.get( "birthday" ), "Birthday not found."
            assert content.get( "email" ), "Email not found"
            assert content.get( "password" ), "Password not found."

            # assert ";" not in content.get( "firstName" ), "Semicolon is present."

            #name input validation
            name = content.get( "name" )

            if len(name) > 44 or len(name) < 2:
                raise Exception("The length of the name is not the correct length.")
            if (name.isalpha() == False):
                raise Exception("The name needs to only contain alphabets.")
        
            #payment input validation
            payment = content.get( "payment" )

            payment_options = ["cash", "credit card", "debit card", "steal"]
            paymment_lower_case = payment.lower()

            if(paymment_lower_case not in payment_options):
                raise Exception("Invalid payment option")

            #birthday input validation
            birthday = content.get( "birthday" )
            # format = "%d-%m-%Y"
            format = "%Y-%m-%d"

            try:
                datetime.strptime(birthday, format)
            except ValueError:
                raise ValueError("The date is not in the correct format.")

            #email input validation 
            email = content.get( "email" )

            if (len(email) > 44):
                raise Exception("The email is too long.")
            if(email.find('@') == -1):
                raise Exception('The email does not contain the "@" character.')

            #password input validation
            password = content.get( "password" )

            if( len(password) < 7):
                raise Exception("The password needs to be more than 7 characters.")

            res = False

            for ele in password:
                if ele.isupper():
                    res = True
                    break
                

            if (res == False):
                raise Exception("The password must contain at least one uppercase character.")
            
            special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            
            if(special_characters.search(password) == None):
                raise Exception('The password must contain at least one special character')

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
    name = event.get('name')
    payment = event.get('payment')
    birthday =  event.get('birthday')
    email = event.get('email')
    password = event.get('password')
    
    #converting birthday to the correct format
    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    birthday = birthday.strftime('%Y-%m-%d %H:%M:%S')

    #generating a unique userid
    userid = uuid.uuid1()

    #hashing the password
    hashed_password = sha256(password.encode('utf-8')).hexdigest()

    # connect to db
    engine = db_connection()

    connection = engine.connect()

    try:
        sql = "INSERT INTO user_info(name, user_id, payment_type, birthday, user_email, user_password) VALUES (%s, %s, %s, %s, %s, %s)" 
        val = (name, userid, payment, birthday, email, hashed_password)
        connection.execute(sql,val)
        
        return MSG_SUCCESS

    except Exception as e:
        print("Email is not unique.")
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "name": "prado",
        "payment": "credit card",
        "birthday": "2020-11-03",
        "email": "prado@ogle.com",
        "password": "Prad#ji"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)