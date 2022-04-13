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
    metadata = db.MetaData()

    # Get User ID from User Email
    user_email = str(event.get('user_email'))
    date_specified = event.get('date_specified')

    user_info = db.Table('user_info', metadata, autoload=True, autoload_with=engine)
    query = db.select(user_info.columns.user_id).where(user_info.columns.user_email == user_email)
    user_id = connection.execute(query).fetchone()

    if user_id:
        user_id = user_id.user_id
    else:
        return MSG_INVALID_ID

    # try:
    events = db.Table('events', metadata, autoload=True, autoload_with=engine)
    query = db.select([events]).where(events.columns.date == date_specified)
    discount = connection.execute(query).fetchone()

    print(discount)

    cart = db.Table('cart', metadata, autoload=True, autoload_with=engine)
    query = db.select(db.func.sum(cart.columns.quantity * cart.columns.price).label('sum_price'))
    query = query.where(cart.columns.user_id == user_id and cart.columns.order_number == 0)
    result = connection.execute(query).fetchone()

    print(result)
    
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
        "date_specified": "2022-04-11"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)