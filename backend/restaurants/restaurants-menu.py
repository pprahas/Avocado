import sqlalchemy as db
import json

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Menu has been retrived successfully.", "body": {}}
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

    rest_id = event.get('rest_id')
    

    # connect to db
    engine = db_connection()

    connection = engine.connect()
    
    sql = "SELECT * FROM avocado1.menu_info WHERE rest_id = %s;"
    val  = rest_id
    result = connection.execute(sql, val).fetchall()
   
   

    result_list = []

    for food in result:
        result_list.append(
            {
                "food_id": food.food_id,
                "food_name": food.food_name,
                "price" : food.price,
                "rating" : food.rating
            }
        )
    #
    # for res in result_list:
    #     print(res)

    MSG_SUCCESS['body'] = result_list
       

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
        "rest_id": "1111"       
    }

    event = {
        "body": json.dumps(body)
     }
    context = ""

    response = lambda_handler(event, context)
    print(response)
   
        
