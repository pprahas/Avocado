from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
import sqlite3

app = Flask(__name__)
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class rest_info(db.Model):
    name = db.Column(db.String(45))
    rest_id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Float())

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

class restInfoScheme(ma.Schema):

    class Meta:
        fields = ('name','rest_id','rating')

rest_info_schema = restInfoScheme()
rest_infos_schema = restInfoScheme(many = True)

@app.route('/get', methods = ['GET'])
def get_all_rest_info():
    # all_rest_info = rest_info.query.all()
    return jsonify({"Restaurant": "Info"})


if __name__ == "__main__":
    app.run(debug = True)
