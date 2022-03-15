import json
import sqlalchemy as db
import datetime

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Discount applied.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Discount Applied Failed.", "body": {}}
MSG_INVALID_ID = {"status": 422, "statusText": "Invalid ID.", "body": {}}

def db_connection():
    username = "admin"
    password = "avocado123"
    server = "avocado-348.cgooazgc1htx.us-east-1.rds.amazonaws.com"
    database = "avocado1"

    db_url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
    engine = db.create_engine(db_url, echo=False)
    engine.connect()

    return engine

# Check for Input
def input_checking(func):
    def inner(event, context):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            assert content.get( "user_email" ), "User Email not found"

        except Exception as e:
            # return data
            return {"status": 422, "statusText": "Account field missing.", "body": str(e)}

        # return function
        return func(content, context)

    # return
    return inner

# Obtain rows from Order History Table
@input_checking
def lambda_handler(event, context):

    # Connect to DB
    engine = db_connection()
    connection = engine.connect()

    # Get User ID from User Email
    user_email = str(event.get('user_email'))

    sql = "SELECT user_id FROM user_info WHERE user_email = %s;"
    value = (user_email)
    user_id = connection.execute(sql, value).fetchone()

    if user_id:
        user_id = user_id.user_id
    else:
        return MSG_INVALID_ID

    try:
        sql = """SELECT sum(quantity) as total_quantity FROM cart 
                where user_id = %s;
        """
        value = (user_id)
        result = connection.execute(sql, value).fetchone()

        MSG_SUCCESS['body'] = {
            "quantity": int(result.total_quantity)
        }

        return MSG_SUCCESS
    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_email": "munhong@gmail.com",
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)