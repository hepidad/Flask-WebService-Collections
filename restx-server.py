import uuid

from flask import Flask, jsonify
from peewee import *
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('carsweb.db')
carsns = api.namespace('cars', description='CARS API operations')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carid = TextField()
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def index():
    return "Server Ready: flask_restx"

@carsns.route('/')
class Car(Resource):

    @api.doc('get all cars list')
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]

        for row in rows:
            datas.append({
            'carid':row.carid,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice
        })
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

        car_create = TBCarsWeb.create(
            carid = uuid.uuid4(),
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice
        )

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'carid':row.carid,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
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

        car_update= TBCarsWeb.update(
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice
            ).where(TBCarsWeb.carid==fId)

        car_update.execute()

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'carid':row.carid,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
        return jsonify(datas)

    def delete(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carid')

        parserGetData = parserData.parse_args()

        fId = parserGetData.get('carid') 

        car_delete = TBCarsWeb.delete().where(TBCarsWeb.carid==fId)
        car_delete.execute()

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'carid':row.carid,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
        return jsonify(datas)

if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5055
        )