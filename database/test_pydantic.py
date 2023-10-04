from flask import Flask
from sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
# db.init_app(app)
# api = Api(app, version='1.0', title='User API', description='A simple User API')

# Define SQLAlchemy model and Pydantic models
class DataRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg1 = db.Column(db.Integer)




# # Create a Namespace for your API
# user_ns = api.namespace('users', description='User operations')

# # Define API models using fields
# register = api.model('UserCreate', {
#     'username': fields.String(required=True, description='Username'),
#     'email': fields.String(required=True, description='Email')
# })



# # Define API endpoints using Resource
# @user_ns.route('/')
# class UserResource(Resource):
#     @api.expect(register)
#     def post(self):
#         """Create a new user"""
#         user_data = api.payload
#         user_create = DataRegister(**user_data)

#         # Check if the email already exists
#         existing_user = DataRegister.query.filter_by(email=user_create.email).first()
#         if existing_user:
#             return {'message': 'Email already exists'}, 400

#         new_user = DataRegister(username=user_create.username, email=user_create.email)
#         db.session.add(new_user)
#         db.session.commit()

#         # Return the new user
#         return make_response({"message": "done"}), 201




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)