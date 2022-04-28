import json
import sqlalchemy as db


MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "Rest Search successful.", "body": {}}
MSG_REST_NOT_FOUND = {"status": 422, "statusText": "Restaurant not found.", "body": {}}


def input_checking(func):
    def inner(event, context):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

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


def checking_user_exist(conn, user_id):
    # check self's table

    sql = """
      select * from person where email = %s;
    """
    value = (user_id)
    result_id = conn.execute(sql, value).fetchone()

    if not result_id:
        sql = """
        select * from person where person_id = %s;
        """
        value = int(user_id)
        result_id = conn.execute(sql, value).fetchone()

    return result_id


@input_checking
def lambda_handler(event, context):
    # TODO implement
    bucket_name = 'avocado-bucket-1'

    # connect to db
    engine = db_connection()
    conn = engine.connect()
    search_key = event.get("search_key")

    search_result = []
    
    # start with search
    value = (search_key + '%' + '%')
    sql = "select * from rest_info where name like '{}'".format(value)
    start_with_search = conn.execute(sql)
    search_result.extend(start_with_search)

    # second word start with search
    value = ("%% " + search_key + "%%")
    sql = "select * from rest_info where name like '{}'".format(value)
    sec_start_with_search = conn.execute(sql)
    search_result.extend(sec_start_with_search)

    # contains       
    value = ("%%" + search_key + "%%")
    sql = "select * from rest_info where name like '{}'".format(value)
    con_start_with_search = conn.execute(sql)
    search_result.extend(con_start_with_search)

    temp_list = []
    for i in search_result:
        if i not in temp_list:
            temp_list.append(i)

    search_result = temp_list

    final_result = []

    index = 0
    for result in search_result:
        final_result.append(
            {
                "rest_id": result.rest_id,
                "rest_name": result.name
            }
        )        
        index += 1
        if index == 5:
            break

    try:
        MSG_SUCCESS['body'] = final_result

        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_REST_NOT_FOUND

#input from the front end
if __name__ == "__main__":
    body = {
        "search_key": "k"
    }
   
    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)
