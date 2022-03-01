import json
import sqlalchemy as db
import datetime

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
            assert content.get( "firstName" ), "First Name not found"
            assert content.get( "lastName" ), "Last Name not found"
            assert content.get( "email" ), "Email not found."
            assert content.get( "birthday" ), "Birthday not found."
            assert content.get( "password" ), "Password not found."

            # assert ";" not in content.get( "firstName" ), "Semicolon is present."

            #firstName input validation
            firstName = content.get( "firstName" )

            if len(firstName) > 30 and len(firstName < 2):
                raise Exception("The length of the first name is not the correct length.")
            if (firstName.isalpha() == False):
                raise Exception("The first name needs to only contain alphabets.")
            
            #lastName input validation
            lastName = content.get( "lastName" )
            if len(lastName) > 30 and len(lastName < 2):
                raise Exception("The length of the first name is not the correct length.")
            if (lastName.isalpha() == False):
                raise Exception("The first name needs to only contain alphabets.")
            
            #email input validation
            
            email = content.get( "email" )
            birthday = content.get( "birthday" )
            password = content.get( "password" )
            if len(firstName) > 4:
                raise Exception("FirstName is longer than 60 characters")

        except Exception as e:
            # return data
            return { "status": 422, "statusText": "Account field missing.", "body": str( e ) }

        # return function
        return func( event, context )

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

    # connect to db
    engine = db_connection()

    connection = engine.connect()

    # metadata = db.MetaData()
    # host = db.Table("host", metadata, autoload=True, autoload_with=engine)


    try:
        # rows = connection.execute(
        # """
        # SELECT * FROM host
        # """)

        # for r in rows:
        #     print(r)

        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE



if __name__ == "__main__":
    body = {
        "firstName": "Jff343",
        "lastName": "Fong",
        "email": "dwejio@google.com",
        "birthday": "02-05-2020",
        "password": "djweoij"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)