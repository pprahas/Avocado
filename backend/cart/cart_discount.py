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
            assert content.get( "date_specified" ), "Date specified not found"

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
    date_specified = event.get('date_specified')

    sql = "SELECT user_id FROM user_info WHERE user_email = %s;"
    value = (user_email)
    user_id = connection.execute(sql, value).fetchone()

    if user_id:
        user_id = user_id.user_id
    else:
        return MSG_INVALID_ID

    # try:
    sql = "SELECT * FROM events WHERE date = %s;"
    value = (date_specified)
    discount = connection.execute(sql, value).fetchone()

    sql = """SELECT sum(quantity*price) as sum_price FROM cart 
            where user_id = %s;
    """
    value = (user_id)
    result = connection.execute(sql, value).fetchone()
    
    event_name = discount.event_name if discount else "",
    discount_amount = discount.discount_amount if discount else 0,
    total_price = result.sum_price if result.sum_price else 0,

    MSG_SUCCESS['body'] = {
        "discount_name": event_name[0],
        "discount_percent": discount_amount[0],
        "total_price": total_price[0] * ((100 - discount_amount[0])/100)
    }

    return MSG_SUCCESS
    # except Exception as e:
    #     print(e)
    #     return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_email": "munhong@gmail.com",
        "date_specified": "2022-03-15"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)