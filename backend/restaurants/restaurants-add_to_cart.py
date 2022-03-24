import sqlalchemy as db
import json

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_ADD_SUCCESS = {"status": 200, "statusText": "The item has been added into cart successfully.", "body": {}}
MSG_UPDATE_SUCCESS = {"status": 200, "statusText": "Quantity updated in cart successfully.", "body": {}}
MSG_ID_NOT_FOUND = {"status": 422, "statusText": "User ID not found.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Add to cart failed.", "body": {}}

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
            return { "status": 422, "statusText": "Restaurant ID field missing.", "body": str( e ) }

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
    # TODO implement
    user_email = event.get('user_email')
    rest_id = int(event.get('rest_id'))
    food_id = int(event.get('food_id'))
    

    # connect to db
    engine = db_connection()

    connection = engine.connect()
    #getting user_id from user_info and rest_name from rest_info
    sql = "SELECT user_id FROM avocado1.user_info WHERE user_email = %s;"
    val  = user_email
    user_id = connection.execute(sql, val).fetchone()
    
    if not user_id:
        return MSG_ID_NOT_FOUND

    user_id = user_id.user_id


    try:
        rest_sql = "SELECT * FROM rest_info WHERE rest_id = %s;"
        val = (rest_id)
        restaurant = connection.execute(rest_sql, val).fetchone()

        menu_sql = "SELECT * FROM menu_info WHERE rest_id = %s AND food_id = %s;"
        val = (rest_id, food_id)
        food = connection.execute(menu_sql, val).fetchone()
        
        #saving cart row
        #check if menu already exist in cart
        cart_checking_sql = "SELECT * FROM cart WHERE user_id = '" + str(user_id) +"' AND food_id = " +str(food_id) + " and order_number = 0" + ";"
        #val3 = (user_id, food_id)
        
        order = connection.execute(cart_checking_sql).fetchall()
        
        #이 트라이는 항상 있어야 함
        if not (order):
            print('okay')
            sql4 = "INSERT INTO cart(user_id,food_id,quantity, price, food_name, rest_id, rest_name, order_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);" 
            # val = (user_id, food_id, 1, food.price, food.name, rest_id, )
            val = (user_id, food_id, 1, food.price, food.food_name, rest_id, restaurant.name, 0)
            connection.execute(sql4, val)

            return MSG_ADD_SUCCESS

        else:
            sql5 = "SELECT quantity FROM avocado1.cart WHERE food_id = " + str(food_id) + " and order_number = 0"
            numFood = connection.execute(sql5).fetchone()
            numFood = numFood[0]

            sql6 = "UPDATE cart set quantity = %s WHERE food_id = %s and order_number = 0"
            value = (numFood+1, food_id)
            connection.execute(sql6, value)

            return MSG_UPDATE_SUCCESS

    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE



if __name__ == "__main__":

    body = {
        "user_email": "munhong@gmail.com",
        "rest_id": "1001",     
        "food_id": "122" 
    }

    event = {
        "body": json.dumps(body)
     }
    context = ""

    response = lambda_handler(event, context)
    print(response)
   
        
