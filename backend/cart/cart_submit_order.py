import uuid
import json
import sqlalchemy as db
from datetime import date
import cart_list_of_items as Cart

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}

# # Establish Connection
# from main import MSG_REQUEST_INCORRECT_FORMAT


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
            assert content.get( "user_id" ), "User ID not found"
            assert content.get( "options" ), "Option not found"
            pass

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

    user_id = int(event.get('user_id'))
    option = int(event.get('options'))

    today = date.today()
    status = 1
    order_number = uuid.uuid4().int % 2147483647

    cart = Cart.lambda_handler(event, context)

    print(cart['body'])

    # sql = "INSERT INTO order_history(order_number, user_id, rest_id, price, options, status, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # value = (order_number, user_id, rest_id, price, option, status, today)

    # connection.execute(sql, value)
    print("\nSuccessfully submited order\n")

    try:
        return MSG_SUCCESS
    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_id": "5000",
        "options": "1"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)