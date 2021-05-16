from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import abort

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0000@localgost/post'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    price = db.Column(db.Integer)
    country = db.Column(db.String(10))
    year = db.Column(db.Integer)
    capasity = db.Column(db.Integer)
    purpose = db.Column(db.String(10))
    size_in_sq_m = db.Column(db.Integer)

    def __init__(self, name, price, country, year,
                 capasity, purpose, size_in_sq_m):
        self.name = name
        self.price = price
        self.country = country
        self.year = year
        self.capasity = capasity
        self.purpose = purpose
        self.size_in_sq_m = size_in_sq_m


class BuildingsSchema(ma.Schema):
    class Meta:
        fields = ('name', 'price', 'country', 'year', 'capasity', 'purpose', 'size_in_sq_m')


building_schema = BuildingsSchema()
buildings_schema = BuildingsSchema(many=True)


@app.route("/buildings", methods=["GET"])
def get_buildings():
    buildings = Building.query.all()
    result = buildings_schema.dump(buildings)
    return jsonify(result)


@app.route("/buildings/<id>", methods=["GET"])
def get_building(id):
    building = Building.query.get(id)
    if building is None:
        abort(404)
    return building_schema.jsonify(building)


@app.route("/buildings", methods=["POST"])
def add_building():
    data = BuildingsSchema().load(request.json)
    new_building = Building(**data)

    db.session.add(new_building)
    db.session.commit()

    return building_schema.jsonify(new_building)


@app.route("/Buildings/<id>", methods=["PUT"])
def update_building(id):
    building = Building.query.get(id)

    if building is None:
        abort(404)

    data = BuildingsSchema().load(request.json)

    for i in data:
        setattr(building, i, request.json[i])

        db.session.commit()
        return building_schema.jsonify(building)


@app.route("/buildings/<id>", methods=["DELETE"])
def delete_building(id):
    building = Building.query.get(id)
    if building is None:
        abort(404)
    db.session.delete(building)
    db.session.commit()
    return building_schema.jsonify(building)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
