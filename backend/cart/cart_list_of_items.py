import json
import sqlalchemy as db

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Cart return successfully.", "body": {}}
MSG_FAIL_RETURN_CART = {"status": 422, "statusText": "Cart return failed.", "body": {}}
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
    user_id = connection.execute(sql, value).fetchone()
    
    if (len(user_id)):
        user_id = user_id.user_id
    else:
        return MSG_USER_NOT_EXIST

    sql = "SELECT * FROM cart WHERE user_id = %s and order_number = 0;"
    value = (user_id)
    result = connection.execute(sql, value).fetchall()

    food_list = []
    
    for rows in result:
        # if order has been placed don't display
        if rows.order_number != 0:
            continue

        sql = "SELECT filepath_s3 FROM menu_info WHERE food_id = %s;"
        value = (rows.food_id)
        food_image = connection.execute(sql, value).fetchone()

        food_list.append(
            {
                "rest_name": rows.rest_name,
                "rest_id": rows.rest_id,
                "food_name": rows.food_name,
                "food_id": rows.food_id,
                "price": rows.price,
                "quantity": rows.quantity,
                "img": food_image.filepath_s3
                # "image": "https://{}.s3.amazonaws.com/{}".format(bucket_name, row.filepath_s3)
            }
        )

    MSG_SUCCESS['body'] = food_list

    try:
        return MSG_SUCCESS
    except Exception as e:
        print(e)
        return MSG_FAIL_RETURN_CART


if __name__ == "__main__":
    body = {
        # "user_email": "davis@purdue.edu"
        "user_email": "munhong@gmail.com"
    }
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)