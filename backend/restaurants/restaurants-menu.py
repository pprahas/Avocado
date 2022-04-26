import sqlalchemy as db
import json
import requests

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

    sql2 = "SELECT * FROM rest_info WHERE rest_id = %s;"
    val2  = rest_id
    rest_name = connection.execute(sql2, val2).fetchone()
    rest_name = rest_name.name
   
    bucket_name = 'avocado-bucket-1'

    result_dict = {
        "pic": [],
        "no_pic": []
    }

    counter = 0
    for food in result:

        response = requests.get("https://{}.s3.amazonaws.com/{}".format(bucket_name, 'MENU/{}/{}.png'.format(rest_id, food.food_id)))

        if response.status_code == 200:
            #IMAGES FOUND
            result_dict["pic"].append(
                {
                    "rest_name": rest_name,
                    "food_id": food.food_id,
                    "food_name": food.food_name,
                    "price" : food.price,
                    "rating" : food.rating,
                    "image": "https://{}.s3.amazonaws.com/{}".format(bucket_name, 'MENU/{}/{}.png'.format(rest_id, food.food_id))
                }
            )
        else:
            #NO IMAGES FOUND
            result_dict["no_pic"].append(
                {
                    "rest_name": rest_name,
                    "food_id": food.food_id,
                    "food_name": food.food_name,
                    "price" : food.price,
                    "rating" : food.rating
                }
            )
            
        counter += 1

    MSG_SUCCESS['body'] = result_dict
       

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
        "rest_id": "1003"       
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)
   
        
