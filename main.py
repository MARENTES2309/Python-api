from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/marentes_python'
db = SQLAlchemy(app)

class PersonaModel(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

args_persona = reqparse.RequestParser()
args_persona.add_argument('name',type=str, help='Name is required', required=True)
args_persona.add_argument('email',type=str, help='Email is required', required=True)

def abort_if_name_exist(name):
    result = PersonaModel.query.filter_by(name=name).first()
    if result:
        abort(404, message='Name already exists.')

def abort_if_email_exist(email):
    result = PersonaModel.query.filter_by(email=email).first()
    if result:
        abort(404, message='Email already exists.')

class Persona(Resource):
    def get(self):
        result = PersonaModel.query.all()
        result = [{'id':i.id,'name':i.name, 'email':i.email} for i in result]
        return jsonify(result)
    
    def post(self):
        args = args_persona.parse_args()
        abort_if_name_exist(args.name)
        abort_if_email_exist(args.email)
        person = PersonaModel(name=args.name,email=args.email)
        db.session.add(person)
        db.session.commit()
        return args, 201
    
api.add_resource(Persona, '/persona')


if __name__ == '__main__':
    app.run(debug=True)