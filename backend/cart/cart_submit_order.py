import uuid
import json
import sqlalchemy as db
from datetime import date

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Submit order successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Submit order failed.", "body": {}}
MSG_USER_NOT_EXIST = {"status": 422, "statusText": "User does not exist.", "body": {}}


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
            assert content.get( "user_email" ), "User ID not found"
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
    metadata = db.MetaData()

    user_email = event.get('user_email')
    option = int(event.get('options'))

    today = date.today()
    status = 1

    # fail safe id
    order_number = 0
    for i in range(3):
        order_number = uuid.uuid4().int % 2147483647
        if order_number != 0:
            break

    user_info = db.Table('user_info', metadata, autoload=True, autoload_with=engine)

    query = db.select(user_info.columns.user_id).where(user_info.columns.user_email == user_email)
    user_id = connection.execute(query).fetchone()
    
    if user_id:
        user_id = user_id.user_id
    else:
        return MSG_USER_NOT_EXIST

    cart = db.Table('cart', metadata, autoload=True, autoload_with=engine)
    # query = db.select(cart).where(cart.columns.user_id == user_id and cart.columns.order_number == 0)
    query = db.select(cart).where(db.and_(cart.columns.user_id == user_id, cart.columns.order_number == 0))
    result = connection.execute(query).fetchall()

    rest_id_list = []

    order_history = db.Table('order_history', metadata, autoload=True, autoload_with=engine)
    for cart_item in result:
        # print(cart_item)
        if cart_item.rest_id not in rest_id_list:
            # insert in order history
            sql = "INSERT INTO order_history(order_number, user_id, rest_id, price, options, status, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (order_number, cart_item.user_id, cart_item.rest_id, cart_item.price, option, status, today)
            connection.execute(sql, value)
            # query = db.insert(order_history).values(order_number= order_number, 
            #                             user_id= cart_item.user_id, 
            #                             rest_id= cart_item.rest_id, 
            #                             price= cart_item.price, 
            #                             options= option, 
            #                             status= status, 
            #                             order_date =today)
            # connection.execute(query) 

            rest_id_list.append(cart_item.rest_id)

        # delete from cart
        sql = "UPDATE cart set order_number = %s WHERE user_id = %s and rest_id = %s and food_id = %s and order_number = 0"
        value = (order_number, cart_item.user_id, cart_item.rest_id, cart_item.food_id)
        connection.execute(sql, value)

        # sql = db.update(cart).values(order_number = order_number).where(db.and_(cart.c.user_id == cart_item.user_id,
        #                                                                          cart.c.rest_id == cart_item.rest_id, 
        #                                                                          cart.c.order_number == 0))
        # connection.execute(sql)

        MSG_SUCCESS['body'] = result
    
    try:
        return MSG_SUCCESS
    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_email": "munhong@gmail.com",
        "options": "1"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)