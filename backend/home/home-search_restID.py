import json
from unicodedata import category
from unittest import result
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
    rest_name = event.get("rest_name")

    # start with search
    sql = "select * from rest_info where name = '{}'".format(rest_name)
    result = conn.execute(sql).fetchone()

    try:
        MSG_SUCCESS['body'] = result.rest_id

        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_REST_NOT_FOUND


# input from the front end
if __name__ == "__main__":
    body = {
        "rest_name": "Kimchi Restaurant"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)
