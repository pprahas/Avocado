from base64 import encode
import json
from operator import imod
import sqlalchemy as db
import datetime
from hashlib import sha256
import datetime
from datetime import date
from datetime import timedelta
import random
import sqlite3
import boto3
import base64
from PIL import Image
from io import BytesIO


MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}
MSG_ORDER_AGAIN_FAIL = {"status": 600, "statusText": "Order again table is unavailable.", "body": {}}

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
            return { "status": 422, "statusText": "Account field missing.", "body": str( e ) }

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
    
    sql = "SELECT * FROM rest_info WHERE rating > 4.0 ORDER BY rating DESC LIMIT 5;"

    #connect to db
    engine = db_connection()
    connection = engine.connect()
    rows = connection.execute(sql)
    popular_rest = []

    #s3 initialization
    s3 = boto3.resource('s3')
    bucket_name = 'avocado-bucket-1'

    #Initializinf stuff for resizing
    FIXED_WIDTH = 300
    FIXED_HEIGHT = 200
    resize = 0.1


    for row in rows:
        #getting string to frontend
        filename = row.filepath_s3
        s3_object = s3.Bucket(bucket_name).Object(filename).get()
        encoded_string_to_frontend = base64.b64encode(s3_object['Body'].read())

        #resizing image
        img = Image.open(BytesIO(base64.b64decode(encoded_string_to_frontend)))
        resize = FIXED_WIDTH/img.size[0] if (FIXED_WIDTH/img.size[0] > FIXED_HEIGHT/img.size[1]) else FIXED_HEIGHT/img.size[1]

        x = img.size[0]
        y = img.size[1]

        img = img.resize(( int(x*resize), int(y*resize)),Image.ANTIALIAS)

        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())

        #print(img_str)

        #getting table of required restaurants
        popular_rest.append(
            #s3 template thingy HERE
            {
                "rest_id": row.rest_id,
                "rest_name": row.name,
                "rest_type": row.rest_type,
                "rating": row.rating,
            }
        )

    try:
        return popular_rest

    except Exception as e:
        print(e)
        return MSG_ORDER_AGAIN_FAIL  



if __name__ == "__main__":
    body = {
        "name": "john doe",
        "user_id": "183269",
        "payment_type": "Cash13",
        "birthday": "2022-02-28",
        "user_email": "tempemail@gmail.com",
        "user_password": "pwefwf@2ht3"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)