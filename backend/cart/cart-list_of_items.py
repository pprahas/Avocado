import json
import sqlalchemy as db
import getDiscount as DC

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}

# Establish Connection
from main import MSG_REQUEST_INCORRECT_FORMAT


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

    user_email = str(event.get('user_email'))

    sql = "SELECT user_id FROM user_info WHERE user_email = %s;"
    value = (user_email)
    user_id = connection.execute(sql, value).fetchall()


    if (len(user_id)):
        user_id = (user_id[0][0])
    else:
        user_id = ""

    sql = "SELECT * FROM cart WHERE user_id = %s;"
    value = (user_id)
    result = connection.execute(sql, value).fetchall()

    food_list = []

    discount = DC.lambda_handler(event, context)
    discount_price = 0.0
    total_price = 0.0

    if (len(discount['body'])):
        discount_price = discount['body'][0]['price']

    for rows in result:
        sql = "SELECT filepath_s3 FROM menu_info WHERE food_id = %s;"
        value = (rows.food_id)
        food_image = connection.execute(sql, value)
        image_path = ""


        for row in food_image:
            image_path = row[0]

        food_list.append(
            {
                "rest_name": rows.rest_name,
                "rest_id": rows.rest_id,
                "food_name": rows.food_name,
                "price": rows.price * rows.quantity,
                "quantity": rows.quantity,
                "img": image_path
            }
        )
        total_price += (rows.price * rows.quantity)

    food_list.append({"discount": discount_price})
    food_list.append({"total_price": total_price - discount_price})

    MSG_SUCCESS['body'] = food_list

    try:
        return MSG_SUCCESS
    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_email": "davis@purdue.edu"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)