from base64 import encode
import json
import sqlalchemy as db
import smtplib
import uuid

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "The unique code has been sent to the user.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "The user's email address does not exist.", "body": {}}

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
            assert content.get( "user_email" ), "Email address not found."
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
   
    #retrieving from the json file 
    user_email = event.get('user_email')

    # connect to db
    engine = db_connection()
    connection = engine.connect()

    #checking if the email exists

    user_email_query_count = "SELECT COUNT(user_id) FROM avocado1.user_info where user_email = \'" + user_email + "\';"
    # print (user_id_query_count)
        
    user_email_db_count = connection.execute(user_email_query_count)

    # print(user_id_db_count)

    for row in user_email_db_count:
        user_email_count = row[0]
    
    # print(user_id_count)

    if(user_email_count == 0):
           return MSG_FAIL_TO_CREATE
    
    # generate unique id
    unique_id = uuid.uuid4().hex

    # sender email address
    email_user = 'cs348avocado@gmail.com'
 
    # sender email password for login purposes
    email_password = 'Cs348-avocado'

    email_send = [user_email]
    subject = 'Forgot your password?'
    msg = MIMEMultipart()
    msg['From'] = email_user
    # converting list of recipients into comma separated string
    msg['To'] = ", ".join(email_send)
    msg['Subject'] = subject

    body = """
    Hello!

    Looks like you've forgotten your password.

    Good news, you can reset it by entering the unique code that you see below:

    """

    body = body + unique_id

    body = body + """

    If you didn't request your password to be reset, just ignore this email.

    Team Avocado Out
    """
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
   
    try:
        server.starttls()
        server.login(email_user,email_password)

        server.sendmail(email_user,email_send,text)

        server.quit()
        return MSG_SUCCESS

    except Exception as e:
        print(e)
        return MSG_FAIL_TO_CREATE


if __name__ == "__main__":
    body = {
        "user_email": "p.prahas@gmaifl.com"
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)

"""
Completed: Currently this code checks if the user_email exists and then sends an email with a
           unique code
Next Step: Instead of creating a new table to store the unique codes for a particular user. Generating
           a temp password and sending that over to the email sounds better to me
"""
             