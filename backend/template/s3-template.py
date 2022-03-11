
import base64
import boto3
import json

# base64 url to pass data through API


# get data from frontend and save data onto s3 
# frontend will send base64 url (file_data), file_name
with open("Transcript Fall 2021.pdf", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())

print(type(encoded_string))

# s3 = boto3.resource('s3')
# bucket_name = 'avocado-bucket-1'
# filename = 'MENU/new.pdf'
# filename = 'RESTAURANTS/new.pdf'

# obj = s3.Object(bucket_name, filename)
# location = obj.put(Body=base64.b64decode(encoded_string))

# with open('json_data.json', 'w') as outfile:
#     json.dump(location, outfile, indent=4, sort_keys=True, default=str)


# # get data from s3 and send it back to frontend
# s3 = boto3.resource('s3')
# s3_object = s3.Bucket(bucket_name).Object(filename).get()
# encoded_string_to_frontend = base64.b64encode(s3_object['Body'].read())
# print(encoded_string_to_frontend[:50])
