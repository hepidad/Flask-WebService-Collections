import uuid
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse
import firebase_admin
from firebase_admin import credentials, db

# Load konfigurasi dari berkas .env
load_dotenv()

app = Flask(__name__)
api = Api(app)

# Dapatkan nilai konfigurasi dari berkas .env
database_url = os.getenv("DATABASE_URL")
project_id = os.getenv("PROJECT_ID")
service_account_path = "flask-api-a4156-firebase-adminsdk-n8hs8-7c4fe30891.json"  # Ubah dengan path berkas service account key "PATH_TO_SERVICE_ACCOUNT_JSON"
# Inisialisasi Admin SDK Firebase
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': database_url,
    'databaseAuthVariableOverride': None
})

# Referensi ke Firebase Realtime Database
db_ref = db.reference()

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carid = TextField(primary_key=True)
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])


@app.route('/')
def index():
    return "Server Ready: flask_restful"

class Car(Resource):
    def get(self):
        cars = db.child('cars').get()
        datas = []

        for car in cars.each():
            datas.append(car.val())
        
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')

        parserGetData = parserData.parse_args()

        fName = parserGetData.get('carname')
        fBrand = parserGetData.get('carbrand')
        fModel = parserGetData.get('carmodel')
        fPrice = parserGetData.get('carprice')

        car_data = {
            'carid': str(uuid.uuid4()),
            'carname': fName,
            'carbrand': fBrand,
            'carmodel': fModel,
            'carprice': fPrice
        }

        db.child('cars').push(car_data)

        cars = db.child('cars').get()
        datas = []

        for car in cars.each():
            datas.append(car.val())
        
        return jsonify(datas)

    def put(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carid')
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')

        parserGetData = parserData.parse_args()

        fId = parserGetData.get('carid')
        fName = parserGetData.get('carname')
        fBrand = parserGetData.get('carbrand')
        fModel = parserGetData.get('carmodel')
        fPrice = parserGetData.get('carprice')

        car_data = {
            'carname': fName,
            'carbrand': fBrand,
            'carmodel': fModel,
            'carprice': fPrice
        }

        db.child('cars').child(fId).update(car_data)

        cars = db.child('cars').get()
        datas = []

        for car in cars.each():
            datas.append(car.val())
        
        return jsonify(datas)

    def delete(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carid')

        parserGetData = parserData.parse_args()

        fId = parserGetData.get('carid') 

        db.child('cars').child(fId).remove()

        cars = db.child('cars').get()
        datas = []

        for car in cars.each():
            datas.append(car.val())
        
        return jsonify(datas)

api.add_resource(Car, '/cars/', endpoint="cars/")

if __name__ == '__main__':
    create_tables()
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5055
    )
