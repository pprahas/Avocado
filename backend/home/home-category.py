import json
from operator import imod
import sqlalchemy as db

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Return home category successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}
MSG_ORDER_AGAIN_FAIL = {"status": 600, "statusText": "Order again table is unavailable.", "body": {}}

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
    rest_type = event.get('rest_type')

    sql = "SELECT * FROM rest_info WHERE rest_type = \"{}\" ORDER BY rating DESC LIMIT 5;".format(rest_type)

    #connect to db
    engine = db_connection()
    connection = engine.connect()
    rows = connection.execute(sql)
    req_rest = []

    bucket_name = 'avocado-bucket-1'

    for row in rows:

        req_rest.append(
            {
                "rest_id": row.rest_id,
                "rest_name": row.name,
                "rest_type": row.rest_type,
                "rating": row.rating,
                "image": "https://{}.s3.amazonaws.com/RESTAURANTS/{}/a.png".format(bucket_name, row.rest_id)
            }
        )

        MSG_SUCCESS['body'] = req_rest

    try:
        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_ORDER_AGAIN_FAIL   




if __name__ == "__main__":
    body = {
        "rest_type": "Asian",
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)