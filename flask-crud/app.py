from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from os import environ
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='User API',
          description='A simple User API')

ns = api.namespace('users', description='User operations')


employee_model = api.model('Employee', {
    'id': fields.Integer(readonly=True, description="L'identifiant unique de l'employé"),
    'first_name': fields.String(required=True, description="Le prénom de l'employé"),
    'last_name': fields.String(required=True, description="Le nom de famille de l'employé"),
    'email': fields.String(required=True, description="L'email de l'employé"),
    'position': fields.String(required=True, description="Le poste de l'employé"),
    'department': fields.String(required=True, description="Le département de l'employé"),
    'salary': fields.Float(required=True, description="Le salaire de l'employé"),
    'created_at': fields.DateTime(readonly=True, description="La date de création de l'enregistrement")
})


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'position': self.position,
            'department': self.department,
            'salary': self.salary,
            'created_at': self.created_at
        }


def init_db():
    with app.app_context():
        db.create_all()


@ns.route('/')
class EmployeeList(Resource):
    @ns.doc('list_employees')
    @ns.marshal_list_with(employee_model)
    def get(self):
        '''Lister tous les employés'''
        return Employee.query.all()

    @ns.doc('create_employee')
    @ns.expect(employee_model)
    @ns.marshal_with(employee_model, code=201)
    def post(self):
        '''Créer un nouvel employé'''
        data = api.payload
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            position=data['position'],
            department=data['department'],
            salary=data['salary'],
            created_at=datetime.datetime.now()
        )
        db.session.add(new_employee)
        db.session.commit()
        return new_employee, 201


@ns.route('/<int:id>')
@ns.response(404, 'Employé non trouvé')
@ns.param('id', "L'identifiant de l'employé")
class EmployeeResource(Resource):
    @ns.doc('get_employee')
    @ns.marshal_with(employee_model)
    def get(self, id):
        '''Récupérer un employé par son identifiant'''
        return Employee.query.get_or_404(id)

    @ns.doc('update_employee')
    @ns.expect(employee_model)
    @ns.marshal_with(employee_model)
    def put(self, id):
        '''Mettre à jour un employé par son identifiant'''
        employee = Employee.query.get_or_404(id)
        data = api.payload
        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        employee.email = data['email']
        employee.position = data['position']
        employee.department = data['department']
        employee.salary = data['salary']
        db.session.commit()
        return employee

    @ns.doc('delete_employee')
    @ns.response(204, 'Employé supprimé')
    def delete(self, id):
        '''Supprimer un employé par son identifiant'''
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


@ns.route('/health/ready')
@ns.response(200, 'Système prêt')
class ReadinessResource(Resource):
    @ns.doc('readiness')
    def get(self):
        '''Vérifier la disponibilité du système'''
        return "Ready"


@ns.route('/health/live')
@ns.response(200, 'Système actif')
class LivenessResource(Resource):
    @ns.doc('liveness')
    def get(self):
        '''Vérifier la vitalité du système'''
        return "Alive"


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
