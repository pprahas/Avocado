from matplotlib import use
import sqlalchemy as db
import json

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "The item has been addedd into cart successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Menu creation failed.", "body": {}}

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
    rest_id = event.get('rest_id')
    food_id = event.get('food_id')
    food_name = event.get('food_name')
    price = event.get('price')

    

    # connect to db
    engine = db_connection()

    connection = engine.connect()
    #getting user_id from user_info and rest_name from rest_info
    sql = "SELECT user_id FROM avocado1.user_info WHERE user_email = %s;"
    val  = user_email
    user_id = connection.execute(sql, val).fetchone()
    
    if user_id == None:
        MSG_REQUEST_NO_BODY['body'] = "No matching User ID from User email"
        return MSG_REQUEST_NO_BODY
    user_id = user_id[0]
    print(user_id)

    sql2 = "SELECT name FROM avocado1.rest_info WHERE rest_id = %s;"
    rest_name = connection.execute(sql2, rest_id).fetchone()
    rest_name = rest_name[0]
    print(rest_name)

    #saving cart row
        #check if menu already exist in cart
    sql3 = "SELECT * FROM avocado1.cart WHERE user_id = '" + str(user_id) +"' AND food_id = " +str(food_id)+";"
    #val3 = (user_id, food_id)
    
    checkExist = connection.execute(sql3).fetchall()

    print(checkExist)
    #print(checkExist)
    if (checkExist == None):
        sql4 = "INSERT INTO avocado1.cart(user_id,food_id,quantity, price, food_name,rest_id, rest_name) VALUES (%s, %s, %s, %s, %s, %s, %s);" 
        val = (user_id, food_id, 1, price, food_name, rest_id,rest_name)
        connection.execute(sql4, val)
    else:
        sql5 = "SELECT quantity FROM avocado1.cart WHERE food_id = " + str(food_id)
        numFood = connection.execute(sql5).fetchone()
        numFood = numFood[0]

        sql6 = "UPDATE cart SET quantity = "+str(numFood+1) +" WHERE food_id = " + str(food_id)
        connection.execute(sql6)

   

    # result_list = []

    # for food in result:
    #     result_list.append(
    #         {
    #             "food_id": food.food_id,
    #             "food_name": food.food_name,
    #             "price" : food.price,
    #             "rating" : food.rating
    #         }
    #     )
    #
    # for res in result_list:
    #     print(res)

    #MSG_SUCCESS['body'] = checkExist
       

    #이 트라이는 항상 있어야 함
    try:

        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE



if __name__ == "__main__":
    
    #  engine = db_connection()

    #  connection = engine.connect()
    
    #  sql = '''SELECT * FROM avocado1.menu_info;'''
    #  result = connection.execute(sql).fetchall()
    # # index 1 is menu 3 is price
    #  menu_dic = {}
    #  for i in result:
    #     menu = str(i[1])
    #     price = i[3]
    #     menu_dic.update({menu:price})
    #  print(menu_dic)

    body = {
        "user_email": "davis@purdue.edu",
        "rest_id": "1008",     
        "food_id": "1010" ,
        "food_name": "a",
        "price": "12.87"
    }

    event = {
        "body": json.dumps(body)
     }
    context = ""

    response = lambda_handler(event, context)
    print(response)
   
        
