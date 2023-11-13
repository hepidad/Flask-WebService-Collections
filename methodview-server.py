import uuid

from flask import Flask, jsonify
from flask.views import MethodView
from peewee import *

#For the sake of parse 
#Using webargs --> https://webargs.readthedocs.io/en/latest/
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)


db = SqliteDatabase('carsweb.db')

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
    return "Server Ready. Tools:flask MethodView"

class Car(MethodView):
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

    @use_args({
        "carname": fields.Str(required=True),
        "carbrand": fields.Str(required=True),
        "carmodel": fields.Str(required=True),
        "carprice": fields.Str(required=True),
        }, 
        location="query")
    def post(self,args):
        fName = args["carname"]
        fBrand = args["carbrand"]
        fModel = args["carmodel"]
        fPrice = args["carprice"]

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

    @use_args({
        "carid": fields.Str(required=True),
        "carname": fields.Str(required=True),
        "carbrand": fields.Str(required=True),
        "carmodel": fields.Str(required=True),
        "carprice": fields.Str(required=True),
        }, 
        location="query")
    def put(self,args):
        fId = args["carid"]
        fName = args["carname"]
        fBrand = args["carbrand"]
        fModel = args["carmodel"]
        fPrice = args["carprice"]

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

    @use_args({"carid": fields.Str(required=True)}, location="query")
    def delete(self, args):
        fId = args["carid"]

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

class CarSearch(MethodView):

    @use_args({"carid": fields.Str(required=True)}, location="query")
    def get(self, args):
    
        fId = args["carid"]

        rows1 = TBCarsWeb.select().where(TBCarsWeb.carid==str(fId))   
        datas=[] 

        for row in rows1:
            datas.append({
            'carid':row.carid,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice
        })
        return jsonify(datas)

app.add_url_rule("/cars/", view_func=Car.as_view('rows'))
app.add_url_rule("/carsearch/", view_func=CarSearch.as_view('rows1'))

if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5055
        )