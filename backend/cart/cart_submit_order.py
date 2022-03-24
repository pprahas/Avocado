import sqlalchemy as db
from datetime import date

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Submit order successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Submit order failed.", "body": {}}
MSG_USER_NOT_EXIST = {"status": 422, "statusText": "User does not exist.", "body": {}}


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
            return {"status": 422, "statusText": "Restaurant ID field missing.", "body": str(e)}

        # return function
        return func(content, context)

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
    user_email = event.get('user_email')
    rest_id = int(event.get('rest_id'))
    food_id = int(event.get('food_id'))

    # connect to db
    engine = db_connection()

    connection = engine.connect()
    # getting user_id from user_info and rest_name from rest_info
    sql = "SELECT user_id FROM avocado1.user_info WHERE user_email = %s;"
    val = user_email
    user_id = connection.execute(sql, val).fetchone()

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

    sql = "SELECT user_id FROM user_info WHERE user_email = %s;"
    value = (user_email)
    user_id = connection.execute(sql, value).fetchone()
    
    if (len(user_id)):
        user_id = user_id.user_id
    else:
        return MSG_USER_NOT_EXIST

    sql = "SELECT * FROM cart WHERE user_id = %s and order_number = 0;"
    value = (user_id)
    result = connection.execute(sql, value).fetchall()


    rest_id_list = []

    for cart_item in result:
        print(cart_item)
        if cart_item.rest_id not in rest_id_list:
            # insert in order history
            sql = "INSERT INTO order_history(order_number, user_id, rest_id, price, options, status, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (order_number, cart_item.user_id, cart_item.rest_id, cart_item.price, option, status, today)
            connection.execute(sql, value)

            rest_id_list.append(cart_item.rest_id)

        # delete from cart
        sql = "UPDATE cart set order_number = %s WHERE user_id = %s and rest_id = %s and food_id = %s and order_number = 0"
        value = (order_number, cart_item.user_id, cart_item.rest_id, cart_item.food_id)
        connection.execute(sql, value)
    
    try:
        if not (order):
            print('okay')
            sql4 = "INSERT INTO cart(user_id,food_id,quantity, price, food_name, rest_id, rest_name) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            # val = (user_id, food_id, 1, food.price, food.name, rest_id, )
            val = (user_id, food_id, 1, food.price, food.food_name, rest_id, restaurant.name)
            connection.execute(sql4, val)

            return MSG_ADD_SUCCESS

        else:
            sql5 = "SELECT quantity FROM avocado1.cart WHERE food_id = " + str(food_id)
            numFood = connection.execute(sql5).fetchone()
            numFood = numFood[0]

            sql6 = "UPDATE cart SET quantity = " + str(numFood + 1) + " WHERE food_id = " + str(food_id)
            connection.execute(sql6)
            return MSG_UPDATE_SUCCESS

    except Exception as e:
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


